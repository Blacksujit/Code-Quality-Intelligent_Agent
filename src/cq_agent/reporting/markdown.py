from __future__ import annotations

from pathlib import Path
from typing import List, Tuple

from cq_agent.analyzers.issue import Issue


def build_markdown_text(root: Path, summary: dict, issues: List[Issue], hotspots: List[Tuple[str, float]] | None = None) -> str:
	lines: list[str] = []
	lines.append(f"# Code Quality Report\n")
	lines.append(f"Path: `{root}`\n")
	lines.append("")
	lines.append(f"## Overview\n")
	lines.append(f"- **files**: {summary.get('file_count', 0)}")
	lines.append(f"- **SLOC**: {summary.get('sloc_total', 0)}")
	lines.append("")
	if hotspots:
		lines.append("## Hotspots (top 10)\n")
		for path, score in hotspots[:10]:
			lines.append(f"- `{path}` — score: {score:.2f}")
		lines.append("")
	lines.append("## Top Issues\n")
	for it in issues[:50]:
		lines.append(f"- **[{it['severity']}] {it['source']} / {it['category']}** — `{it['file']}:{it['start_line']}` — {it['title']}")
		if it.get("description"):
			lines.append(f"  - {it['description']}")
		if it.get("suggested_fix"):
			lines.append(f"  - Suggested fix: {it['suggested_fix']}")
		if it.get("references"):
			ref = ", ".join([r for r in it["references"] if r])
			if ref:
				lines.append(f"  - References: {ref}")
		lines.append("")
	return "\n".join(lines)


def write_markdown_report(out_path: Path, root: Path, summary: dict, issues: List[Issue], hotspots: List[Tuple[str, float]] | None = None) -> None:
	text = build_markdown_text(root, summary, issues, hotspots)
	out_path.write_text(text, encoding="utf-8")
