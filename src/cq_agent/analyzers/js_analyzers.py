from __future__ import annotations

import json
import shutil
import subprocess
from pathlib import Path
from typing import List

from .issue import Issue, normalize_severity


ESLINT_DEFAULT_CMD = [
	"npx", "--yes", "eslint", ".", "-f", "json",
]


def _run_cmd(cmd: list[str], cwd: Path) -> tuple[int, str, str]:
	try:
		res = subprocess.run(cmd, cwd=str(cwd), capture_output=True, text=True, timeout=120)
		return res.returncode, res.stdout, res.stderr
	except Exception as e:
		return 1, "", str(e)


def analyze_js_ts(root: Path) -> List[Issue]:
	# Try eslint via npx; if unavailable or errors, return empty list gracefully
	if shutil.which("npx") is None:
		return []
	code, out, err = _run_cmd(ESLINT_DEFAULT_CMD, root)
	if code not in (0, 1):
		return []
	issues: List[Issue] = []
	try:
		data = json.loads(out or "[]")
		for file_entry in data:
			file_path = file_entry.get("filePath", "")
			for m in file_entry.get("messages", []):
				sev = normalize_severity({2: "high", 1: "medium"}.get(m.get("severity", 1), "medium"))
				issues.append(Issue(
					id=f"eslint:{m.get('ruleId','')}:{file_path}:{m.get('line',0)}",
					title=f"ESLint {m.get('ruleId','')}",
					description=m.get("message", ""),
					category="style",
					severity=sev,
					confidence="high",
					file=file_path,
					start_line=int(m.get("line", 0)),
					end_line=int(m.get("endLine", m.get("line", 0))),
					evidence="",
					suggested_fix="",
					references=[],
					source="eslint",
					tags=["lint"],
				))
	except Exception:
		return []
	return issues
