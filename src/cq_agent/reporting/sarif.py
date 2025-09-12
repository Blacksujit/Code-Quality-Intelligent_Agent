from __future__ import annotations

import json
from pathlib import Path
from typing import List

from cq_agent.analyzers.issue import Issue


def write_sarif(out_path: Path, root: Path, issues: List[Issue]) -> None:
	runs = [
		{
			"tool": {
				"driver": {
					"name": "cq-agent",
					"informationUri": "https://example.com",
					"rules": []
				}
			},
			"results": [
				{
					"ruleId": it.get("id", ""),
					"level": _sev_to_level(it.get("severity", "medium")),
					"message": {"text": it.get("description", it.get("title", ""))},
					"locations": [
						{
							"physicalLocation": {
								"artifactLocation": {"uri": _rel_uri(root, it.get("file", ""))},
								"region": {
									"startLine": it.get("start_line", 1),
									"endLine": it.get("end_line", it.get("start_line", 1)),
								}
							}
						}
					]
				}
				for it in issues
			],
		}
	]
	payload = {"version": "2.1.0", "$schema": "https://json.schemastore.org/sarif-2.1.0.json", "runs": runs}
	out_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")


def _sev_to_level(sev: str) -> str:
	sev = sev.lower()
	if sev == "critical":
		return "error"
	if sev == "high":
		return "error"
	if sev == "medium":
		return "warning"
	return "note"


def _rel_uri(root: Path, file_path: str) -> str:
	try:
		p = root / file_path
		return p.as_posix()
	except Exception:
		return file_path
