from __future__ import annotations

import json
import shutil
import subprocess
from pathlib import Path
from typing import List, Sequence

from .issue import Issue, normalize_severity


def _run_cmd(cmd: list[str], cwd: Path) -> tuple[int, str, str]:
	try:
		res = subprocess.run(cmd, cwd=str(cwd), capture_output=True, text=True, timeout=60)
		return res.returncode, res.stdout, res.stderr
	except Exception as e:
		return 1, "", str(e)


def run_ruff(root: Path) -> List[Issue]:
	if shutil.which("ruff") is None:
		return []
	code, out, err = _run_cmd(["ruff", "check", "--output-format", "json"], root)
	if code not in (0, 1):
		return []
	issues: List[Issue] = []
	try:
		data = json.loads(out or "[]")
		for it in data:
			issues.append(Issue(
				id=f"ruff:{it.get('code','')}:{it.get('filename','')}:{it.get('location',{}).get('row',0)}",
				title=f"Ruff {it.get('code','')}",
				description=it.get("message", ""),
				category="style",
				severity=normalize_severity("warning"),
				confidence="high",
				file=it.get("filename", ""),
				start_line=int(it.get("location", {}).get("row", 0)),
				end_line=int(it.get("end_location", {}).get("row", it.get("location", {}).get("row", 0))),
				evidence="",
				suggested_fix="",
				references=[],
				source="ruff",
				tags=["lint"],
			))
	except Exception:
		return []
	return issues


def run_bandit(root: Path) -> List[Issue]:
	if shutil.which("bandit") is None:
		return []
	code, out, err = _run_cmd(["bandit", "-r", ".", "-f", "json"], root)
	if code not in (0, 1):
		return []
	issues: List[Issue] = []
	try:
		data = json.loads(out or "{}")
		for res in data.get("results", []):
			sev = normalize_severity(res.get("issue_severity", "medium"), default="medium")
			issues.append(Issue(
				id=f"bandit:{res.get('test_id','')}:{res.get('filename','')}:{res.get('line_number',0)}",
				title=f"Bandit {res.get('test_id','')}",
				description=res.get("issue_text", ""),
				category="security",
				severity=sev,
				confidence="high",
				file=res.get("filename", ""),
				start_line=int(res.get("line_number", 0)),
				end_line=int(res.get("line_number", 0)),
				evidence=res.get("code", ""),
				suggested_fix="",
				references=[res.get("more_info", "")],
				source="bandit",
				tags=["security"],
			))
	except Exception:
		return []
	return issues


def run_radon_cc(root: Path) -> List[Issue]:
	# Cyclomatic complexity via radon, mark high complexity as issues
	if shutil.which("radon") is None:
		return []
	code, out, err = _run_cmd(["radon", "cc", "-j", "-n", "C", "."], root)
	if code not in (0, 1):
		return []
	issues: List[Issue] = []
	try:
		data = json.loads(out or "{}")
		for file_path, entries in data.items():
			for ent in entries:
				rank = ent.get("rank", "C")
				sev = "medium" if rank == "C" else ("high" if rank in ("D", "E") else "critical")
				issues.append(Issue(
					id=f"radon:{rank}:{file_path}:{ent.get('lineno',0)}",
					title=f"High complexity ({rank})",
					description=f"Block {ent.get('name','')} has cyclomatic complexity {ent.get('complexity','?')} (rank {rank}).",
					category="complexity",
					severity=sev,  # type: ignore[assignment]
					confidence="medium",
					file=file_path,
					start_line=int(ent.get("lineno", 0)),
					end_line=int(ent.get("endline", ent.get("lineno", 0))),
					evidence="",
					suggested_fix="Consider refactoring into smaller functions or reducing branching.",
					references=["https://radon.readthedocs.io/en/latest/commandline.html#radon-cc"],
					source="radon",
					tags=["complexity"],
				))
	except Exception:
		return []
	return issues


def analyze_python(root: Path) -> List[Issue]:
	issues: List[Issue] = []
	issues.extend(run_ruff(root))
	issues.extend(run_bandit(root))
	issues.extend(run_radon_cc(root))
	return issues


# Targeted runs (fast mode): allow restricting to a subset of files
def run_ruff_on_files(root: Path, files: Sequence[str]) -> List[Issue]:
	if shutil.which("ruff") is None or not files:
		return []
	cmd = ["ruff", "check", "--output-format", "json", *files]
	code, out, err = _run_cmd(cmd, root)
	if code not in (0, 1):
		return []
	issues: List[Issue] = []
	try:
		data = json.loads(out or "[]")
		for it in data:
			issues.append(Issue(
				id=f"ruff:{it.get('code','')}:{it.get('filename','')}:{it.get('location',{}).get('row',0)}",
				title=f"Ruff {it.get('code','')}",
				description=it.get("message", ""),
				category="style",
				severity=normalize_severity("warning"),
				confidence="high",
				file=it.get("filename", ""),
				start_line=int(it.get("location", {}).get("row", 0)),
				end_line=int(it.get("end_location", {}).get("row", it.get("location", {}).get("row", 0))),
				evidence="",
				suggested_fix="",
				references=[],
				source="ruff",
				tags=["lint"],
			))
	except Exception:
		return []
	return issues


def run_bandit_on_paths(root: Path, files: Sequence[str]) -> List[Issue]:
	if shutil.which("bandit") is None or not files:
		return []
	# Bandit can accept file paths; fall back to -r . if too many
	cmd: list[str]
	if len(files) > 200:
		cmd = ["bandit", "-r", ".", "-f", "json"]
	else:
		cmd = ["bandit", "-f", "json", *files]
	code, out, err = _run_cmd(cmd, root)
	if code not in (0, 1):
		return []
	issues: List[Issue] = []
	try:
		data = json.loads(out or "{}")
		for res in data.get("results", []):
			sev = normalize_severity(res.get("issue_severity", "medium"), default="medium")
			issues.append(Issue(
				id=f"bandit:{res.get('test_id','')}:{res.get('filename','')}:{res.get('line_number',0)}",
				title=f"Bandit {res.get('test_id','')}",
				description=res.get("issue_text", ""),
				category="security",
				severity=sev,  # type: ignore[assignment]
				confidence="high",
				file=res.get("filename", ""),
				start_line=int(res.get("line_number", 0)),
				end_line=int(res.get("line_number", 0)),
				evidence=res.get("code", ""),
				suggested_fix="",
				references=[res.get("more_info", "")],
				source="bandit",
				tags=["security"],
			))
	except Exception:
		return []
	return issues
