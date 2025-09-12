from __future__ import annotations

import ast
import re
from collections import defaultdict
from pathlib import Path
from typing import Dict, List, Set, Tuple

from cq_agent.ingestion import RepoContext


_IMPORT_RE = re.compile(r"^\s*import\s+([\w\./\-@]+)|^\s*from\s+([\w\./\-@]+)\s+import", re.MULTILINE)
_JS_IMPORT_RE = re.compile(r"import\s+.*?from\s+['\"]([^'\"]+)['\"]|require\(['\"]([^'\"]+)['\"]\)")


def _py_imports(text: str) -> Set[str]:
	imports: Set[str] = set()
	try:
		tree = ast.parse(text)
		for node in ast.walk(tree):
			if isinstance(node, ast.Import):
				for alias in node.names:
					imports.add(alias.name.split(".")[0])
			elif isinstance(node, ast.ImportFrom):
				if node.module:
					imports.add(node.module.split(".")[0])
	except Exception:
		# Fallback to regex if ast fails
		for m in _IMPORT_RE.finditer(text):
			pkg = m.group(1) or m.group(2)
			if pkg:
				imports.add(pkg.split(".")[0])
	return imports


def _js_imports(text: str) -> Set[str]:
	imports: Set[str] = set()
	for m in _JS_IMPORT_RE.finditer(text):
		pkg = m.group(1) or m.group(2)
		if not pkg:
			continue
		imports.add(pkg)
	return imports


def build_dependency_graph(repo: RepoContext) -> Dict[str, Set[str]]:
	# Graph is file-level: file -> set(dependencies)
	graph: Dict[str, Set[str]] = defaultdict(set)
	for rel_path, rec in repo["files"].items():
		lang = rec.get("language")
		text: str = rec.get("text", "")
		if lang == "python":
			imports = _py_imports(text)
			# naive mapping: import name to files containing that name in path
			for other_path in repo["files"].keys():
				base = Path(other_path).stem
				if base in imports and other_path != rel_path:
					graph[rel_path].add(other_path)
		elif lang in ("javascript", "typescript"):
			imports = _js_imports(text)
			for imp in imports:
				if imp.startswith("./") or imp.startswith("../"):
					# resolve relative to approximate file match
					candidate = str(Path(rel_path).parent.joinpath(imp))
					# try matching any file that startswith candidate
					for other_path in repo["files"].keys():
						if other_path.startswith(candidate):
							graph[rel_path].add(other_path)
				else:
					# package import, skip
					pass
		else:
			continue
	# ensure all nodes appear
	for p in repo["files"].keys():
		graph.setdefault(p, set())
	return graph


def compute_hotspots(repo: RepoContext, graph: Dict[str, Set[str]]) -> List[Tuple[str, float]]:
	# Score = normalized churn + normalized SLOC + degree centrality (out+in)
	files = list(repo["files"].keys())
	if not files:
		return []
	sloc_map = {p: repo["files"][p]["sloc"] for p in files}
	churn_map = repo["git"].get("churn_by_file", {})

	# in-degree
	in_degree: Dict[str, int] = defaultdict(int)
	for src, deps in graph.items():
		for dst in deps:
			in_degree[dst] += 1

	out_degree = {p: len(graph.get(p, set())) for p in files}

	def _norm(value_map: Dict[str, int]) -> Dict[str, float]:
		vals = list(value_map.values())
		max_v = max(vals) if vals else 1
		if max_v == 0:
			return {k: 0.0 for k in value_map}
		return {k: v / max_v for k, v in value_map.items()}

	n_sloc = _norm(sloc_map)
	n_churn = _norm({p: int(churn_map.get(p, 0)) for p in files})
	n_central = _norm({p: in_degree.get(p, 0) + out_degree.get(p, 0) for p in files})

	scores = []
	for p in files:
		score = 0.5 * n_churn.get(p, 0.0) + 0.3 * n_sloc.get(p, 0.0) + 0.2 * n_central.get(p, 0.0)
		scores.append((p, score))
	# sort by score desc
	return sorted(scores, key=lambda x: x[1], reverse=True)
