from __future__ import annotations

"""
Agentic Q&A over a repository using LangChain (and optionally LangGraph).

This module builds a light agent that:
1) Retrieves top context chunks via the existing TF-IDF/Hybrid index
2) Runs a reasoning+answer prompt with an LLM backend

Backends supported:
- "local": LangChain + Ollama (no API key)
- "deepseek": uses existing DeepSeek integration for direct answer

If LangGraph is available, we may expand to multi-step workflows later.
"""

from typing import Optional, List, Tuple, Sequence
import re

from cq_agent.ingestion import RepoContext
from cq_agent.qa.index import build_index


def _gather_context(repo: RepoContext, question: str, top_k: int = 6) -> List[str]:
    index = build_index(repo)
    hits = index.search(question, top_k=top_k)
    chunks: List[str] = []
    for ch, _ in hits:
        chunks.append(f"{ch.path}:{ch.start_line}-{ch.end_line}\n{ch.text}")
    return chunks


# --- Prompt utilities -------------------------------------------------------

def _infer_bullet_count(question: str, default_count: int = 5) -> int:
    match = re.search(r"\b(\d{1,2})\b", question)
    if match:
        try:
            n = int(match.group(1))
            if 1 <= n <= 12:
                return n
        except Exception:
            pass
    return default_count


def _looks_like_code_or_html(text: str) -> bool:
    t = text.strip().lower()
    if (
        "```" in t
        or "<html" in t
        or "</" in t
        or t.startswith("#")
        or "<!doctype" in t
        or "<script" in t
        or "<style" in t
    ):
        return True
    # Heuristic for repeated code-like lines
    return bool(re.search(r"\bdef\s+|\bclass\s+|;\s*$|\{\s*$|\}\s*$", t, re.MULTILINE))


def _is_unhelpful(text: str) -> bool:
    t = (text or "").strip().lower()
    if not t:
        return True
    # Obvious placeholders or empty assignments
    if re.fullmatch(r"answer\s*=\s*['\"]?['\"]?", t):
        return True
    # Too short/non-informative after removing non-word chars
    letters = re.sub(r"[^a-z0-9]+", "", t)
    return len(letters) < 4


def _postprocess_to_bullets(text: str, max_bullets: int) -> str:
    # Remove code fences and HTML tags
    cleaned = re.sub(r"```[\s\S]*?```", " ", text)
    cleaned = re.sub(r"<[^>]+>", " ", cleaned)
    cleaned = cleaned.replace("\r", " ")
    # Prefer existing list markers
    lines = re.split(r"[\n\r]+", cleaned)
    items: List[str] = []
    for ln in lines:
        s = ln.strip(" -*•\t")
        if not s:
            continue
        if len(s) < 3:
            continue
        # Treat lines that begin with a bullet or dash as items
        if ln.lstrip().startswith(("-", "*", "•")):
            items.append(s)
    # If no bullets detected, split into sentences
    if not items:
        sentences = re.split(r"(?<=[.!?])\s+", cleaned)
        for s in sentences:
            s2 = s.strip()
            if 3 <= len(s2) <= 220:
                items.append(s2)
    items = [re.sub(r"\s+", " ", it).strip().rstrip("-:;,") for it in items]
    items = [it for it in items if it]
    items = items[:max_bullets]
    if not items:
        return ""
    return "\n".join(f"- {it}" for it in items)


def _answer_with_local(question: str, ctx: List[str], model: str | None) -> Optional[str]:
    try:
        from cq_agent.ai.local_llm import answer_with_local_llm  # type: ignore
    except Exception:
        return None
    return answer_with_local_llm(question, ctx, model or "llama3.1")


def _answer_with_deepseek(question: str, repo: RepoContext, api_key: str) -> Optional[str]:
    try:
        from cq_agent.ai.deepseek import answer_codebase_question  # type: ignore
    except Exception:
        return None
    try:
        return answer_codebase_question(question, repo, api_key)
    except Exception:
        return None


def _answer_with_hf(
    question: str,
    context_chunks: List[str],
    model_id: str,
    history: Optional[Sequence[Tuple[str, str]]] = None,
) -> Optional[str]:
    """Answer using Hugging Face Inference API (no local download)."""
    try:
        from huggingface_hub import InferenceClient  # type: ignore
    except Exception:
        return None
    import os
    token = os.getenv("HUGGINGFACEHUB_API_TOKEN", "")
    if not token:
        return None
    client = InferenceClient(model=model_id, token=token)
    # Build compact prompt with strict formatting instructions
    ctx = "\n\n".join(context_chunks[:6]) or "[No context]"
    # Include brief history transcript (last 3 exchanges)
    hist = list(history or [])[-6:]
    chat_lines: List[str] = []
    for role, content in hist:
        role_tag = "User" if role == "user" else "Assistant"
        chat_lines.append(f"{role_tag}: {content}")
    transcript = "\n".join(chat_lines)
    n_bullets = _infer_bullet_count(question, default_count=5)
    prompt = (
        "System: You are a concise code analysis assistant.\n"
        "Rules:\n- Prefer short, clear sentences.\n- Output Markdown bullet points only.\n"
        "- Cite file paths if relevant.\n- Do NOT output code or HTML unless explicitly requested.\n"
        f"- Produce exactly {n_bullets} bullets when a number is implied; otherwise {n_bullets}.\n\n"
        + (f"Conversation so far:\n{transcript}\n\n" if transcript else "")
        + f"CONTEXT:\n{ctx}\n\nQUESTION: {question}\n"
        + f"ANSWER (exactly {n_bullets} bullets, no code/HTML):"
    )
    try:
        # text_generation works for many text-generation-inference/backends
        out = client.text_generation(prompt, max_new_tokens=256, temperature=0.1, top_p=0.9)
        return out.strip() if isinstance(out, str) else None
    except Exception:
        return None


def _answer_with_hf_router(
    question: str,
    context_chunks: List[str],
    model_id: str,
    history: Optional[Sequence[Tuple[str, str]]] = None,
) -> Optional[str]:
    """Answer using Hugging Face Inference Router (OpenAI-compatible)."""
    import os
    base_url = os.getenv("HF_BASE_URL", "https://router.huggingface.co/v1")
    token = os.getenv("HF_TOKEN", "")
    if not token:
        return None
    try:
        from openai import OpenAI  # type: ignore
    except Exception:
        return None
    client = OpenAI(base_url=base_url, api_key=token)
    ctx = "\n\n".join(context_chunks[:6]) or "[No context]"
    n_bullets = _infer_bullet_count(question, default_count=5)
    system = (
        "You are a concise code analysis assistant. Use CONTEXT to answer QUESTION. "
        "Rules: Output Markdown bullet points only; cite file paths when relevant; no code/HTML unless explicitly requested; "
        f"produce exactly {n_bullets} bullets when a number is implied; otherwise {n_bullets}."
    )
    # Map short recent history into chat messages
    messages = [{"role": "system", "content": system}]
    for role, content in list(history or [])[-6:]:
        role_name = "assistant" if role == "assistant" else "user"
        messages.append({"role": role_name, "content": content})
    user = (
        f"CONTEXT:\n{ctx}\n\nQUESTION: {question}\n"
        f"ANSWER (exactly {n_bullets} bullets, no code/HTML):"
    )
    try:
        messages.append({"role": "user", "content": user})
        resp = client.chat.completions.create(
            model=model_id,
            messages=messages,
            temperature=0.1,
            max_tokens=256,
        )
        msg = getattr(resp.choices[0].message, "content", None) if resp and resp.choices else None
        return msg.strip() if isinstance(msg, str) else None
    except Exception:
        return None


def run_agentic_qa(
    question: str,
    repo: RepoContext,
    backend: str = "extractive",
    model: str | None = None,
    history: Optional[Sequence[Tuple[str, str]]] = None,
) -> Tuple[Optional[str], List[Tuple[str, float]]]:
    """Run an agentic Q&A round and return (answer, references).

    References are returned as a list of (preview, score) for display; the caller
    can also run its own index.search to render richer refs.
    """
    # Collect retrieval context first
    index = build_index(repo)
    search_results = index.search(question, top_k=6)
    context_strings = [f"{ch.path}:{ch.start_line}-{ch.end_line}\n{ch.text}" for ch, _ in search_results]

    answer: Optional[str] = None

    if backend == "deepseek":
        import os
        api_key = os.getenv("DEEPSEEK_API_KEY", "")
        if api_key:
            answer = _answer_with_deepseek(question, repo, api_key)
    elif backend == "local":
        # default to local
        answer = _answer_with_local(question, context_strings, model)
    elif backend == "hf":
        # Prefer HF Router (OpenAI-compatible) if HF_TOKEN is set; otherwise use InferenceClient
        model_id = model or "HuggingFaceH4/zephyr-7b-beta"
        answer = _answer_with_hf_router(question, context_strings, model_id, history=history)
        if not answer:
            answer = _answer_with_hf(question, context_strings, model_id, history=history)
        # Enforce clean formatting; fallback to extractive if code/HTML or unhelpful output
        if answer and (_looks_like_code_or_html(answer) or _is_unhelpful(answer)):
            # Try to post-process into bullets; if still looks bad, clear it
            n_bullets = _infer_bullet_count(question, default_count=5)
            processed = _postprocess_to_bullets(answer, n_bullets)
            if processed and not _looks_like_code_or_html(processed) and not _is_unhelpful(processed):
                answer = processed
            else:
                answer = None
    else:
        # Extractive mode: compose a brief answer from top chunks without an LLM
        # Strategy: pick the top 2-3 chunks, extract the most relevant lines
        # (first non-empty line or lines containing the question keywords), and stitch.
        key = question.lower()
        snippets: List[str] = []
        for ch, _ in search_results[:3]:
            lines = [ln.strip() for ln in ch.text.splitlines() if ln.strip()]
            # Prefer lines that include words from the query
            best_line = None
            for ln in lines:
                if any(w and w in ln.lower() for w in key.split() if len(w) > 3):
                    best_line = ln
                    break
            best_line = best_line or (lines[0] if lines else "")
            if best_line:
                snippets.append(f"{ch.path}:{ch.start_line}-{ch.end_line} → {best_line}")
        if snippets:
            answer = (
                "Extractive summary (no LLM):\n- "
                + "\n- ".join(snippets[:4])
            )

    refs: List[Tuple[str, float]] = []
    for ch, score in search_results:
        preview = " ".join(ch.text.split())[:200]
        refs.append((f"{ch.path}:{ch.start_line}-{ch.end_line}  {preview}", score))

    # If no LLM answer, provide an extractive fallback formatted as bullets
    if not answer or _is_unhelpful(answer):
        n_bullets = _infer_bullet_count(question, default_count=5)
        # Convert refs previews to bullets
        bullets = []
        for preview, _ in refs[:n_bullets]:
            # Keep only the preview text after the path
            parts = preview.split("  ", 1)
            text = parts[1] if len(parts) > 1 else preview
            bullets.append(text)
        if bullets:
            answer = "\n".join(f"- {b}" for b in bullets)

    return answer, refs


