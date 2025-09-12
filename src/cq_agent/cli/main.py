from __future__ import annotations

import os
import warnings

# Reduce noisy framework logs/warnings for a cleaner CLI UX
os.environ.setdefault("TF_CPP_MIN_LOG_LEVEL", "3")  # 0=all, 1=INFO off, 2=WARNING off, 3=ERROR off
os.environ.setdefault("TOKENIZERS_PARALLELISM", "false")
warnings.filterwarnings("ignore", category=UserWarning, module=r"torchvision\..*")
warnings.filterwarnings("ignore", category=UserWarning, module=r"tensorflow\..*")
warnings.filterwarnings("ignore", category=UserWarning, module=r"tf_keras\..*")
warnings.filterwarnings("ignore", category=FutureWarning, module=r"tensorflow\..*")

try:  # Quiet transformers logger if available
	from transformers.utils import logging as hf_logging  # type: ignore
	hf_logging.set_verbosity_error()
except Exception:
	pass

# Silence TensorFlow/absl python loggers
try:
	import logging as _pylog
	_pylog.getLogger("tensorflow").setLevel(_pylog.ERROR)
	from absl import logging as _absllog  # type: ignore
	_absllog.set_verbosity(_absllog.ERROR)
	_absllog.set_stderrthreshold("error")
except Exception:
	pass

import argparse
import sys
from pathlib import Path

from cq_agent.ingestion import load_repo
from cq_agent.analyzers import analyze_python, analyze_js_ts, Issue
from cq_agent.metrics.metrics import detect_near_duplicates, detect_docs_tests_hints
from cq_agent.scoring.score import prioritize_issues
from cq_agent.reporting.markdown import write_markdown_report
from cq_agent.reporting.sarif import write_sarif
from cq_agent.graph.deps import build_dependency_graph, compute_hotspots
from cq_agent.qa.index import build_index
from cq_agent.autofix.auto import compute_autofixes, generate_patch, apply_edits
from cq_agent.ai import enhance_issues_with_ai
try:
	from cq_agent.ai.deepseek import answer_codebase_question  # type: ignore
except Exception:  # pragma: no cover
	answer_codebase_question = None  # type: ignore
try:
	from cq_agent.ai.local_llm import answer_with_local_llm  # type: ignore
except Exception:  # pragma: no cover
	answer_with_local_llm = None  # type: ignore
try:
	from cq_agent.ai.agent_qa import run_agentic_qa  # type: ignore
except Exception:  # pragma: no cover
	run_agentic_qa = None  # type: ignore


def command_analyze(path: str, md: str | None, sarif: str | None, autofix: bool, autofix_dry_run: bool, incremental: bool, workers: int | None, deepseek: bool) -> int:
	root = Path(path).expanduser().resolve()
	if not root.exists():
		print(f"Path not found: {root}")
		return 1
	print(f"[MVP] Analyze started for: {root}")
	repo = load_repo(str(root), incremental=incremental)
	langs = ", ".join(repo["languages"]) or "(none)"
	print(f"Files: {repo['summary']['file_count']} | SLOC: {repo['summary']['sloc_total']} | Languages: {langs}")

	issues: list[Issue] = []
	if "python" in repo["languages"]:
		issues.extend(analyze_python(root))
	if any(lang in repo["languages"] for lang in ("javascript", "typescript")):
		issues.extend(analyze_js_ts(root))
	issues.extend(detect_near_duplicates(repo))
	issues.extend(detect_docs_tests_hints(repo))

	issues = prioritize_issues(issues)
	graph = build_dependency_graph(repo)
	hotspots = compute_hotspots(repo, graph)

	# Optional AI enhancement (DeepSeek)
	if deepseek:
		import os
		api_key = os.getenv("DEEPSEEK_API_KEY", "")
		if api_key:
			try:
				issues = enhance_issues_with_ai(issues, repo, api_key)
				print("[AI] DeepSeek enhancement applied.")
			except Exception as exc:
				print(f"[AI] Skipped (error): {exc}")

	print(f"Issues found: {len(issues)}")
	for it in issues[:10]:
		print(f"- [{it['severity']}] {it['source']} {it['category']} {it['file']}:{it['start_line']} - {it['title']}")

	if md:
		write_markdown_report(Path(md), root, repo["summary"], issues, hotspots)
		print(f"Wrote Markdown report to: {md}")
	if sarif:
		write_sarif(Path(sarif), root, issues)
		print(f"Wrote SARIF report to: {sarif}")

	if autofix or autofix_dry_run:
		edits = compute_autofixes(root, issues)
		print(f"Autofix candidates: {len(edits)}")
		if edits:
			patch_text = generate_patch(edits, root)
			print("--- Autofix unified diff (preview) ---")
			print(patch_text)
			if autofix and not autofix_dry_run:
				results = apply_edits(edits)
				applied = sum(1 for _, ok in results if ok)
				print(f"Applied edits: {applied}/{len(results)}")

	print("[MVP] Analyze completed (prioritized + reports + hotspots + autofix).")
	return 0


def command_qa(path: str, deepseek: bool = False, local_llm: bool = False, local_model: str | None = None, agent: bool = False, agent_backend: str | None = None, agent_model: str | None = None, llama_cpp_model: str | None = None) -> int:
	root = Path(path).expanduser().resolve()
	if not root.exists():
		print(f"Path not found: {root}")
		return 1
	print(f"[MVP] QA over: {root}. Type 'exit' to quit.")
	repo = load_repo(str(root))
	index = build_index(repo)
	# Maintain a short rolling conversation history for agent backends
	history: list[tuple[str, str]] = []
	while True:
		try:
			q = input("Q> ").strip()
		except (EOFError, KeyboardInterrupt):
			print()
			break
		if not q or q.lower() in {"exit", "quit"}:
			break
		# Append user message to conversation history (bounded later)
		history.append(("user", q))
		# Agentic mode takes precedence
		if agent and run_agentic_qa is not None:
			backend = (agent_backend or ("deepseek" if deepseek else "extractive"))
			# Provide a safe default model for HF backend if none was supplied
			if backend == "hf" and not (agent_model or local_model):
				agent_model = "HuggingFaceH4/zephyr-7b-beta"
			try:
				ans, refs = run_agentic_qa(q, repo, backend=backend, model=agent_model or local_model, history=history)
				if ans:
					print(f"A> {ans}")
					# Add assistant reply to conversation history and keep last 6 turns
					history.append(("assistant", ans))
					history = history[-6:]
				elif backend == "hf":
					# Provide diagnostics to help users configure HF correctly
					model_used = (agent_model or local_model or "HuggingFaceH4/zephyr-7b-beta")
					import os as _os
					hf_router = bool(_os.getenv("HF_TOKEN"))
					hf_api = bool(_os.getenv("HUGGINGFACEHUB_API_TOKEN"))
					path = "Router(OpenAI)" if hf_router else ("InferenceAPI" if hf_api else "none")
					print(f"[HF] No answer. path={path} model={model_used} HF_TOKEN={hf_router} HUGGINGFACEHUB_API_TOKEN={hf_api}")
					print("      Tip: Set HF_TOKEN for Router (preferred) OR HUGGINGFACEHUB_API_TOKEN for Inference API; ensure model id has access.")
					print("      Try: --agent-model 'HuggingFaceH4/zephyr-7b-beta:featherless-ai' (Router) or 'HuggingFaceH4/zephyr-7b-beta' (API).")
				# Show references from agent run
				for preview, score in refs:
					print(f"- {preview}  score={score:.3f}")
			except Exception as exc:
				print(f"[Agent] Skipped (error): {exc}")
		# Otherwise DeepSeek AI
		elif deepseek and answer_codebase_question is not None:
			import os
			api_key = os.getenv("DEEPSEEK_API_KEY", "")
			if api_key:
				try:
					answer = answer_codebase_question(q, repo, api_key)
					if answer:
						print(f"A> {answer}")
				except Exception as exc:
					print(f"[AI] Skipped (error): {exc}")
		# Optionally answer via local LLM (LangChain + Ollama)
		elif local_llm and answer_with_local_llm is not None:
			# Build small context from top TF-IDF hits
			hits = index.search(q, top_k=5)
			ctx = []
			for ch, _ in hits:
				ctx.append(f"{ch.path}:{ch.start_line}-{ch.end_line}\n{ch.text}")
			try:
				model_name = llama_cpp_model or local_model or "llama3.1"
				resp = answer_with_local_llm(q, ctx, model=model_name)
				if resp:
					print(f"A> {resp}")
			except Exception as exc:
				print(f"[LocalAI] Skipped (error): {exc}")
		# Always show supporting references
		results = index.search(q, top_k=5)
		for ch, score in results:
			print(f"- {ch.path}:{ch.start_line}-{ch.end_line}  score={score:.3f}")
			preview = " ".join(ch.text.split())[:200]
			print(f"  {preview}")
	return 0


def build_parser() -> argparse.ArgumentParser:
	parser = argparse.ArgumentParser(prog="cq-agent", description="Code Quality Intelligence Agent")
	sub = parser.add_subparsers(dest="command", required=True)

	p_an = sub.add_parser("analyze", help="Analyze a code repository path")
	p_an.add_argument("path", help="Path to code repository")
	p_an.add_argument("--md", help="Write Markdown report to this path")
	p_an.add_argument("--sarif", help="Write SARIF report to this path")
	p_an.add_argument("--autofix", action="store_true", help="Apply safe autofixes in-place")
	p_an.add_argument("--autofix-dry-run", action="store_true", help="Preview safe autofixes as a unified diff")
	p_an.add_argument("--incremental", action="store_true", default=True, help="Use incremental cache and mtimes (default on)")
	p_an.add_argument("--no-incremental", dest="incremental", action="store_false", help="Disable incremental cache")
	p_an.add_argument("--workers", type=int, default=None, help="Override worker threads for ingestion (reserved)")
	p_an.add_argument("--deepseek", action="store_true", help="Enable DeepSeek AI enhancement (requires DEEPSEEK_API_KEY)")

	p_qa = sub.add_parser("qa", help="Interactive Q&A over a code repository")
	p_qa.add_argument("path", help="Path to code repository")
	p_qa.add_argument("--deepseek", action="store_true", help="Enable DeepSeek AI for Q&A (requires DEEPSEEK_API_KEY)")
	p_qa.add_argument("--local-llm", action="store_true", help="Use local LLM via LangChain + Ollama (no API key)")
	p_qa.add_argument("--local-model", help="Ollama model name (default: llama3.1)")
	# Agentic flags
	p_qa.add_argument("--agent", action="store_true", help="Use agentic Q&A (retrieval + reasoning)")
	p_qa.add_argument("--agent-backend", choices=["extractive", "local", "deepseek", "hf"], help="Agent LLM backend (default: extractive; 'hf' uses Hugging Face Inference API)")
	p_qa.add_argument("--agent-model", help="Agent model name (e.g., llama3.1)")
	# llama.cpp GGUF path (enables local backend without Ollama)
	p_qa.add_argument("--llama-cpp-model", help="Path to GGUF model file to use llama.cpp backend")

	return parser


def main(argv: list[str] | None = None) -> int:
	argv = list(sys.argv[1:] if argv is None else argv)
	parser = build_parser()
	args = parser.parse_args(argv)

	if args.command == "analyze":
		return command_analyze(args.path, args.md, args.sarif, args.autofix, args.autofix_dry_run, args.incremental, args.workers, args.deepseek)
	if args.command == "qa":
		return command_qa(
			args.path,
			getattr(args, "deepseek", False),
			getattr(args, "local_llm", False),
			getattr(args, "local_model", None),
			getattr(args, "agent", False),
			getattr(args, "agent_backend", None),
			getattr(args, "agent_model", None),
			getattr(args, "llama_cpp_model", None),
		)

	return 0


if __name__ == "__main__":
	sys.exit(main())
