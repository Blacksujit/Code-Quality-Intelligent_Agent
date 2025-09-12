from __future__ import annotations

import difflib
from dataclasses import dataclass
from pathlib import Path
from typing import List, Tuple

from cq_agent.analyzers.issue import Issue


@dataclass
class FileEdit:
	path: Path
	old_text: str
	new_text: str


def _remove_line(text: str, line_no: int) -> str:
	lines = text.splitlines()
	idx = max(0, line_no - 1)
	if idx < len(lines):
		# Remove the line; leave the rest unchanged
		lines.pop(idx)
	return "\n".join(lines) + ("\n" if text.endswith("\n") else "")


def compute_autofixes(root: Path, issues: List[Issue]) -> List[FileEdit]:
	"""Compute safe autofixes for a subset of rules (currently Ruff F401)."""
	edits: List[FileEdit] = []
	for it in issues:
		if it.get("source") != "ruff":
			continue
		issue_id = it.get("id", "")
		title = it.get("title", "")
		if "F401" not in issue_id and "F401" not in title:
			continue
		file_path = root / it.get("file", "")
		if not file_path.exists():
			continue
		try:
			old_text = file_path.read_text(encoding="utf-8")
		except Exception:
			continue
		new_text = _remove_line(old_text, it.get("start_line", 1))
		if new_text != old_text:
			edits.append(FileEdit(path=file_path, old_text=old_text, new_text=new_text))
	return edits


def generate_patch(edits: List[FileEdit], root: Path) -> str:
	patch_parts: List[str] = []
	for e in edits:
		old = e.old_text.splitlines(keepends=True)
		new = e.new_text.splitlines(keepends=True)
		rel = e.path.relative_to(root).as_posix()
		diff = difflib.unified_diff(old, new, fromfile=f"a/{rel}", tofile=f"b/{rel}")
		patch_parts.append("".join(diff))
	return "".join(patch_parts)


def apply_edits(edits: List[FileEdit]) -> List[Tuple[Path, bool]]:
	results: List[Tuple[Path, bool]] = []
	for e in edits:
		try:
			e.path.write_text(e.new_text, encoding="utf-8")
			results.append((e.path, True))
		except Exception:
			results.append((e.path, False))
	return results
