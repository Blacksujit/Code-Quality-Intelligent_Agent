# Code Quality Report

Path: `E:\Code-Quality-Agent`


## Overview

- **files**: 44
- **SLOC**: 8354

## Hotspots (top 10)

- `src\cq_agent\web\app.py` — score: 0.80
- `src\cq_agent\visualizations\trends.py` — score: 0.46
- `src\cq_agent\web\components.py` — score: 0.31
- `src\cq_agent\analyzers\issue.py` — score: 0.25
- `src\cq_agent\visualizations\__init__.py` — score: 0.24
- `src\cq_agent\analyzers\__init__.py` — score: 0.24
- `src\cq_agent\ai\deepseek.py` — score: 0.24
- `src\cq_agent\agents\reasoning.py` — score: 0.23
- `src\cq_agent\agents\langgraph_trends.py` — score: 0.22
- `src\cq_agent\visualizations\advanced_deps.py` — score: 0.21

## Top Issues

- **[medium] heuristic-dup / duplication** — `src\cq_agent\visualizations\trends.py:1` — Near-duplicate code across files
  - These files appear to share duplicated blocks: src\cq_agent\visualizations\trends.py and src\cq_agent\web\components.py.
  - Suggested fix: Extract common code into a shared function/module.

- **[medium] heuristic-dup / duplication** — `src\cq_agent\visualizations\advanced_deps.py:1` — Near-duplicate code across files
  - These files appear to share duplicated blocks: src\cq_agent\visualizations\advanced_deps.py and src\cq_agent\visualizations\dependency_graph.py.
  - Suggested fix: Extract common code into a shared function/module.

- **[medium] heuristic-dup / duplication** — `src\cq_agent\__main__.py:1` — Near-duplicate code across files
  - These files appear to share duplicated blocks: src\cq_agent\__main__.py and src\cq_agent\cli\main.py.
  - Suggested fix: Extract common code into a shared function/module.

- **[medium] ruff / style** — `E:\Code-Quality-Agent\verify_installation.py:11` — Ruff F401
  - `cq_agent.cli.main.main` imported but unused; consider using `importlib.util.find_spec` to test for availability

- **[medium] ruff / style** — `E:\Code-Quality-Agent\verify_installation.py:7` — Ruff F401
  - `cq_agent` imported but unused; consider using `importlib.util.find_spec` to test for availability

- **[medium] ruff / style** — `E:\Code-Quality-Agent\src\cq_agent\web\components.py:228` — Ruff F841
  - Local variable `e` is assigned to but never used

- **[medium] ruff / style** — `E:\Code-Quality-Agent\src\cq_agent\web\components.py:150` — Ruff E722
  - Do not use bare `except`

- **[medium] ruff / style** — `E:\Code-Quality-Agent\src\cq_agent\web\components.py:142` — Ruff E722
  - Do not use bare `except`

- **[medium] ruff / style** — `E:\Code-Quality-Agent\src\cq_agent\web\app.py:1586` — Ruff F821
  - Undefined name `run_agentic_qa`

- **[medium] ruff / style** — `E:\Code-Quality-Agent\src\cq_agent\web\app.py:1584` — Ruff F821
  - Undefined name `run_agentic_qa`

- **[medium] ruff / style** — `E:\Code-Quality-Agent\src\cq_agent\web\app.py:1582` — Ruff F821
  - Undefined name `run_agentic_qa`

- **[medium] ruff / style** — `E:\Code-Quality-Agent\src\cq_agent\web\app.py:1581` — Ruff F821
  - Undefined name `run_agentic_qa`

- **[medium] ruff / style** — `E:\Code-Quality-Agent\src\cq_agent\web\app.py:1570` — Ruff F821
  - Undefined name `answer_codebase_question`

- **[medium] ruff / style** — `E:\Code-Quality-Agent\src\cq_agent\web\app.py:1443` — Ruff F821
  - Undefined name `create_langgraph_trend_analysis`

- **[medium] ruff / style** — `E:\Code-Quality-Agent\src\cq_agent\web\app.py:1424` — Ruff F821
  - Undefined name `create_trend_visualizations`

- **[medium] ruff / style** — `E:\Code-Quality-Agent\src\cq_agent\web\app.py:1384` — Ruff F821
  - Undefined name `create_hotspot_visualizations`

- **[medium] ruff / style** — `E:\Code-Quality-Agent\src\cq_agent\web\app.py:1248` — Ruff F821
  - Undefined name `create_advanced_dependency_visualizations`

- **[medium] ruff / style** — `E:\Code-Quality-Agent\src\cq_agent\web\app.py:1042` — Ruff F821
  - Undefined name `create_trend_chart`

- **[medium] ruff / style** — `E:\Code-Quality-Agent\src\cq_agent\web\app.py:1039` — Ruff F821
  - Undefined name `create_language_distribution_chart`

- **[medium] ruff / style** — `E:\Code-Quality-Agent\src\cq_agent\web\app.py:1033` — Ruff F821
  - Undefined name `create_hotspots_chart`

- **[medium] ruff / style** — `E:\Code-Quality-Agent\src\cq_agent\web\app.py:1030` — Ruff F821
  - Undefined name `create_severity_chart`

- **[medium] ruff / style** — `E:\Code-Quality-Agent\src\cq_agent\web\app.py:1024` — Ruff F821
  - Undefined name `create_quality_score_gauge`

- **[medium] ruff / style** — `E:\Code-Quality-Agent\src\cq_agent\web\app.py:997` — Ruff F821
  - Undefined name `create_metrics_cards`

- **[medium] ruff / style** — `E:\Code-Quality-Agent\src\cq_agent\web\app.py:913` — Ruff F821
  - Undefined name `run_agentic_qa`

- **[medium] ruff / style** — `E:\Code-Quality-Agent\src\cq_agent\web\app.py:904` — Ruff F821
  - Undefined name `run_agentic_qa`

- **[medium] ruff / style** — `E:\Code-Quality-Agent\src\cq_agent\web\app.py:901` — Ruff F821
  - Undefined name `enhance_issues_with_ai`

- **[medium] ruff / style** — `E:\Code-Quality-Agent\src\cq_agent\web\app.py:892` — Ruff F821
  - Undefined name `run_bandit_on_paths`

- **[medium] ruff / style** — `E:\Code-Quality-Agent\src\cq_agent\web\app.py:891` — Ruff F821
  - Undefined name `run_ruff_on_files`

- **[medium] ruff / style** — `E:\Code-Quality-Agent\src\cq_agent\web\app.py:872` — Ruff F821
  - Undefined name `save_tfidf_index`

- **[medium] ruff / style** — `E:\Code-Quality-Agent\src\cq_agent\web\app.py:871` — Ruff F821
  - Undefined name `build_tfidf_index`

- **[medium] ruff / style** — `E:\Code-Quality-Agent\src\cq_agent\web\app.py:869` — Ruff F821
  - Undefined name `load_tfidf_index`

- **[medium] ruff / style** — `E:\Code-Quality-Agent\src\cq_agent\web\app.py:816` — Ruff F821
  - Undefined name `run_bandit_on_paths`

- **[medium] ruff / style** — `E:\Code-Quality-Agent\src\cq_agent\web\app.py:815` — Ruff F821
  - Undefined name `run_ruff_on_files`

- **[medium] ruff / style** — `E:\Code-Quality-Agent\src\cq_agent\web\app.py:792` — Ruff F821
  - Undefined name `save_tfidf_index`

- **[medium] ruff / style** — `E:\Code-Quality-Agent\src\cq_agent\web\app.py:791` — Ruff F821
  - Undefined name `build_tfidf_index`

- **[medium] ruff / style** — `E:\Code-Quality-Agent\src\cq_agent\web\app.py:789` — Ruff F821
  - Undefined name `load_tfidf_index`

- **[medium] ruff / style** — `E:\Code-Quality-Agent\src\cq_agent\web\app.py:723` — Ruff F821
  - Undefined name `run_agentic_qa`

- **[medium] ruff / style** — `E:\Code-Quality-Agent\src\cq_agent\web\app.py:286` — Ruff E722
  - Do not use bare `except`

- **[medium] ruff / style** — `E:\Code-Quality-Agent\src\cq_agent\web\app.py:254` — Ruff E722
  - Do not use bare `except`

- **[medium] ruff / style** — `E:\Code-Quality-Agent\src\cq_agent\web\app.py:202` — Ruff E722
  - Do not use bare `except`

- **[medium] ruff / style** — `E:\Code-Quality-Agent\src\cq_agent\web\app.py:161` — Ruff E722
  - Do not use bare `except`

- **[medium] ruff / style** — `E:\Code-Quality-Agent\src\cq_agent\web\app.py:29` — Ruff E402
  - Module level import not at top of file

- **[medium] ruff / style** — `E:\Code-Quality-Agent\src\cq_agent\web\app.py:28` — Ruff E402
  - Module level import not at top of file

- **[medium] ruff / style** — `E:\Code-Quality-Agent\src\cq_agent\web\app.py:27` — Ruff E402
  - Module level import not at top of file

- **[medium] ruff / style** — `E:\Code-Quality-Agent\src\cq_agent\visualizations\trends.py:386` — Ruff F541
  - f-string without any placeholders

- **[medium] ruff / style** — `E:\Code-Quality-Agent\src\cq_agent\visualizations\trends.py:356` — Ruff F541
  - f-string without any placeholders

- **[medium] ruff / style** — `E:\Code-Quality-Agent\src\cq_agent\visualizations\trends.py:295` — Ruff F841
  - Local variable `languages` is assigned to but never used

- **[medium] ruff / style** — `E:\Code-Quality-Agent\src\cq_agent\visualizations\trends.py:294` — Ruff F841
  - Local variable `file_count` is assigned to but never used

- **[medium] ruff / style** — `E:\Code-Quality-Agent\src\cq_agent\visualizations\trends.py:293` — Ruff E722
  - Do not use bare `except`

- **[medium] ruff / style** — `E:\Code-Quality-Agent\src\cq_agent\visualizations\trends.py:242` — Ruff F541
  - f-string without any placeholders
