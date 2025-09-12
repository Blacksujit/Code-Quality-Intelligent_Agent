from __future__ import annotations

from typing import Literal, TypedDict, List

Severity = Literal["critical", "high", "medium", "low"]
Category = Literal[
	"security",
	"performance",
	"duplication",
	"complexity",
	"testing",
	"docs",
	"style",
	"correctness",
	"other",
]


class Issue(TypedDict):
	id: str
	title: str
	description: str
	category: Category
	severity: Severity
	confidence: Literal["high", "medium", "low"]
	file: str
	start_line: int
	end_line: int
	evidence: str
	suggested_fix: str
	references: List[str]
	source: str  # analyzer that produced it (e.g., ruff, bandit, eslint)
	tags: List[str]


_SEVERITY_ORDER = {"critical": 3, "high": 2, "medium": 1, "low": 0}


def normalize_severity(score: str | int | None, default: Severity = "medium") -> Severity:
	if score is None:
		return default
	if isinstance(score, int):
		if score >= 9:
			return "critical"
		if score >= 7:
			return "high"
		if score >= 4:
			return "medium"
		return "low"
	text = str(score).lower()
	for key in _SEVERITY_ORDER:
		if key in text:
			return key  # type: ignore[return-value]
	if text in {"error", "err"}:
		return "high"
	if text in {"warn", "warning"}:
		return "medium"
	return default


def clamp_severity(sev: Severity, floor: Severity | None = None) -> Severity:
	if floor is None:
		return sev
	return max(sev, floor, key=lambda s: _SEVERITY_ORDER[s])
