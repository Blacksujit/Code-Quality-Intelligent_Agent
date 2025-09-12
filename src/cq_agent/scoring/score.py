from __future__ import annotations

from typing import List, Tuple

from cq_agent.analyzers.issue import Issue


_SEVERITY_RANK = {"critical": 3, "high": 2, "medium": 1, "low": 0}


def _base_score(issue: Issue) -> int:
	return _SEVERITY_RANK.get(issue["severity"], 0)


def _boosts(issue: Issue) -> int:
	boost = 0
	# Boost security and correctness
	if issue["category"] in ("security", "correctness"):
		boost += 2
	# Slight boost for complexity findings
	if issue["category"] == "complexity":
		boost += 1
	# If from bandit or radon, consider more confident signals
	if issue["source"] in ("bandit", "radon"):
		boost += 1
	return boost


def prioritize_issues(issues: List[Issue]) -> List[Issue]:
	# Compute composite score and sort descending
	scored: List[Tuple[int, Issue]] = []
	for it in issues:
		score = _base_score(it) + _boosts(it)
		scored.append((score, it))
	# Sort by score desc, then file, then line
	ordered = sorted(scored, key=lambda p: (p[0], p[1]["file"], p[1]["start_line"]), reverse=True)
	return [it for _, it in ordered]
