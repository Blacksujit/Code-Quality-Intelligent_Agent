from __future__ import annotations

import hashlib
from pathlib import Path
from typing import Dict, List, Tuple

from cq_agent.analyzers.issue import Issue
from cq_agent.ingestion import RepoContext


def _shingle_hashes(text: str, k: int = 8) -> set[str]:
	lines = [ln.strip() for ln in text.splitlines() if ln.strip()]
	if len(lines) < k:
		return set()
	hashes: set[str] = set()
	for i in range(len(lines) - k + 1):
		window = "\n".join(lines[i : i + k])
		hashes.add(hashlib.sha1(window.encode("utf-8", errors="replace")).hexdigest())
	return hashes


def detect_near_duplicates(repo: RepoContext) -> List[Issue]:
	# Very simple: overlapping shingle hashes across files
	index: Dict[str, List[str]] = {}
	for rel_path, rec in repo["files"].items():
		for h in _shingle_hashes(rec.get("text", "")):
			index.setdefault(h, []).append(rel_path)
	pairs: set[Tuple[str, str]] = set()
	for files in index.values():
		if len(files) < 2:
			continue
		unique = sorted(set(files))
		for i in range(len(unique)):
			for j in range(i + 1, len(unique)):
				pairs.add((unique[i], unique[j]))
	issues: List[Issue] = []
	for a, b in sorted(pairs):
		issues.append(Issue(
			id=f"dup:{a}:{b}",
			title="Near-duplicate code across files",
			description=f"These files appear to share duplicated blocks: {a} and {b}.",
			category="duplication",
			severity="medium",
			confidence="medium",
			file=a,
			start_line=1,
			end_line=1,
			evidence=b,
			suggested_fix="Extract common code into a shared function/module.",
			references=[],
			source="heuristic-dup",
			tags=["duplication"],
		))
	return issues


def detect_docs_tests_hints(repo: RepoContext) -> List[Issue]:
	issues: List[Issue] = []
	# Missing README
	root = Path(repo["root"]).resolve()
	if not (root / "README.md").exists() and not (root / "README.rst").exists():
		issues.append(Issue(
			id="docs:readme",
			title="Repository missing README",
			description="Project does not contain a README file.",
			category="docs",
			severity="low",
			confidence="high",
			file=".",
			start_line=1,
			end_line=1,
			evidence="",
			suggested_fix="Add a README with setup, usage, and architecture notes.",
			references=[],
			source="heuristic-docs",
			tags=["docs"],
		))
	# Missing docstrings in Python files (simple heuristic)
	for rel_path, rec in repo["files"].items():
		if rec.get("language") == "python":
			text = rec.get("text", "")
			if text.strip().startswith('"""') or text.strip().startswith("'''"):
				continue
			issues.append(Issue(
				id=f"docs:docstring:{rel_path}",
				title="Python module missing top-level docstring",
				description="Add a module docstring to explain purpose and usage.",
				category="docs",
				severity="low",
				confidence="medium",
				file=rel_path,
				start_line=1,
				end_line=1,
				evidence="",
				suggested_fix="Add a brief module-level docstring.",
				references=[],
				source="heuristic-docs",
				tags=["docs"],
			))
	return issues
