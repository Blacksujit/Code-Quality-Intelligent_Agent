from __future__ import annotations

"""
Local LLM Q&A using LangChain + Ollama.
Requires local Ollama runtime and a pulled model (e.g., `ollama pull llama3.1`).
Falls back gracefully by returning None if unavailable.
"""

from typing import Optional, List


def _render_prompt(question: str, context_chunks: List[str]) -> str:
    joined_context = "\n\n".join(context_chunks[:8])
    if not joined_context:
        joined_context = "[No context available]"
    template = (
        "You are a helpful code assistant. Answer the user's question using the provided code context.\n"
        "Be concise and specific. If unsure, say you are not certain.\n\n"
        "Context:\n{context}\n\n"
        "Question: {question}\n\n"
        "Answer:"
    )
    try:
        from langchain.prompts import PromptTemplate  # type: ignore
        return PromptTemplate(template=template, input_variables=["context", "question"]).format(
            context=joined_context,
            question=question,
        )
    except Exception:
        return template.format(context=joined_context, question=question)


def answer_with_local_llm(question: str, context_chunks: List[str], model: str = "llama3.1") -> Optional[str]:
    # If model looks like a GGUF file path, prefer llama.cpp backend
    if model and model.lower().endswith(".gguf"):
        try:
            from langchain_community.llms import LlamaCpp  # type: ignore
        except Exception:
            return None
        prompt = _render_prompt(question, context_chunks)
        try:
            llm = LlamaCpp(model_path=model, n_ctx=4096, n_threads=0)
            response = llm.invoke(prompt) if hasattr(llm, "invoke") else llm(prompt)  # type: ignore
            return str(response).strip()
        except Exception:
            return None

    # If model looks like a GPT4All .bin path, use GPT4All backend
    if model and model.lower().endswith(".bin"):
        try:
            from langchain_community.llms import GPT4All  # type: ignore
        except Exception:
            return None
        prompt = _render_prompt(question, context_chunks)
        try:
            llm = GPT4All(model=model, max_tokens=512)
            response = llm.invoke(prompt) if hasattr(llm, "invoke") else llm(prompt)  # type: ignore
            return str(response).strip()
        except Exception:
            return None

    # Prefer modern langchain-ollama backend; fall back to deprecated import if needed
    llm = None
    try:
        from langchain_ollama import OllamaLLM  # type: ignore
        try:
            llm = OllamaLLM(model=model)
        except Exception:
            llm = None
    except Exception:
        try:
            from langchain_community.llms import Ollama  # type: ignore
            try:
                llm = Ollama(model=model)
            except Exception:
                llm = None
        except Exception:
            return None
    if llm is None:
        return None

    prompt = _render_prompt(question, context_chunks)

    try:
        # LangChain interfaces may expose different call methods across versions
        if hasattr(llm, "invoke"):
            response = llm.invoke(prompt)  # type: ignore
        else:
            response = llm(prompt)  # type: ignore
        return response.strip()
    except Exception:
        return None


