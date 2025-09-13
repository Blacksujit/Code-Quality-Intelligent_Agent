# Code Quality Report

Path: `F:\Code-Quality-Agent`


## Overview

- **files**: 39
- **SLOC**: 7479

## Hotspots (top 10)

- `src\cq_agent\web\app.py` — score: 0.80
- `src\cq_agent\cli\main.py` — score: 0.55
- `src\cq_agent\analyzers\issue.py` — score: 0.46
- `src\cq_agent\visualizations\advanced_deps.py` — score: 0.45
- `src\cq_agent\visualizations\__init__.py` — score: 0.45
- `src\cq_agent\analyzers\__init__.py` — score: 0.45
- `src\cq_agent\analyzers\python_analyzers.py` — score: 0.43
- `src\cq_agent\agents\reasoning.py` — score: 0.42
- `src\cq_agent\qa\embeddings.py` — score: 0.41
- `src\cq_agent\visualizations\trends.py` — score: 0.41

## Top Issues

- **[medium] heuristic-dup / duplication** — `src\cq_agent\visualizations\advanced_deps.py:1` — Near-duplicate code across files
  - These files appear to share duplicated blocks: src\cq_agent\visualizations\advanced_deps.py and src\cq_agent\visualizations\dependency_graph.py.
  - Suggested fix: Extract common code into a shared function/module.

- **[medium] ruff / style** — `F:\Code-Quality-Agent\src\cq_agent\web\app.py:42` — Ruff E402
  - Module level import not at top of file

- **[medium] ruff / style** — `F:\Code-Quality-Agent\src\cq_agent\web\app.py:41` — Ruff E402
  - Module level import not at top of file

- **[medium] ruff / style** — `F:\Code-Quality-Agent\src\cq_agent\web\app.py:40` — Ruff E402
  - Module level import not at top of file

- **[medium] ruff / style** — `F:\Code-Quality-Agent\src\cq_agent\web\app.py:39` — Ruff E402
  - Module level import not at top of file

- **[medium] ruff / style** — `F:\Code-Quality-Agent\src\cq_agent\web\app.py:38` — Ruff E402
  - Module level import not at top of file

- **[medium] ruff / style** — `F:\Code-Quality-Agent\src\cq_agent\web\app.py:37` — Ruff E402
  - Module level import not at top of file

- **[medium] ruff / style** — `F:\Code-Quality-Agent\src\cq_agent\web\app.py:36` — Ruff E402
  - Module level import not at top of file

- **[medium] ruff / style** — `F:\Code-Quality-Agent\src\cq_agent\web\app.py:35` — Ruff E402
  - Module level import not at top of file

- **[medium] ruff / style** — `F:\Code-Quality-Agent\src\cq_agent\web\app.py:34` — Ruff E402
  - Module level import not at top of file

- **[medium] ruff / style** — `F:\Code-Quality-Agent\src\cq_agent\web\app.py:33` — Ruff E402
  - Module level import not at top of file

- **[medium] ruff / style** — `F:\Code-Quality-Agent\src\cq_agent\web\app.py:29` — Ruff E402
  - Module level import not at top of file

- **[medium] ruff / style** — `F:\Code-Quality-Agent\src\cq_agent\web\app.py:28` — Ruff E402
  - Module level import not at top of file

- **[medium] ruff / style** — `F:\Code-Quality-Agent\src\cq_agent\web\app.py:27` — Ruff E402
  - Module level import not at top of file

- **[medium] ruff / style** — `F:\Code-Quality-Agent\src\cq_agent\web\app.py:26` — Ruff E402
  - Module level import not at top of file

- **[medium] ruff / style** — `F:\Code-Quality-Agent\src\cq_agent\web\app.py:25` — Ruff E402
  - Module level import not at top of file

- **[medium] ruff / style** — `F:\Code-Quality-Agent\src\cq_agent\web\app.py:24` — Ruff E402
  - Module level import not at top of file

- **[medium] ruff / style** — `F:\Code-Quality-Agent\src\cq_agent\web\app.py:23` — Ruff E402
  - Module level import not at top of file

- **[medium] ruff / style** — `F:\Code-Quality-Agent\src\cq_agent\web\app.py:22` — Ruff E402
  - Module level import not at top of file

- **[medium] ruff / style** — `F:\Code-Quality-Agent\src\cq_agent\web\app.py:15` — Ruff E402
  - Module level import not at top of file

- **[medium] ruff / style** — `F:\Code-Quality-Agent\src\cq_agent\web\app.py:14` — Ruff E402
  - Module level import not at top of file

- **[medium] ruff / style** — `F:\Code-Quality-Agent\src\cq_agent\web\app.py:13` — Ruff E402
  - Module level import not at top of file

- **[medium] ruff / style** — `F:\Code-Quality-Agent\src\cq_agent\visualizations\trends.py:440` — Ruff F821
  - Undefined name `Dict`

- **[medium] ruff / style** — `F:\Code-Quality-Agent\src\cq_agent\visualizations\trends.py:225` — Ruff F821
  - Undefined name `Dict`

- **[medium] ruff / style** — `F:\Code-Quality-Agent\src\cq_agent\visualizations\trends.py:203` — Ruff F541
  - f-string without any placeholders

- **[medium] ruff / style** — `F:\Code-Quality-Agent\src\cq_agent\visualizations\trends.py:151` — Ruff F841
  - Local variable `languages` is assigned to but never used

- **[medium] ruff / style** — `F:\Code-Quality-Agent\src\cq_agent\visualizations\trends.py:150` — Ruff F841
  - Local variable `file_count` is assigned to but never used

- **[medium] ruff / style** — `F:\Code-Quality-Agent\src\cq_agent\visualizations\trends.py:149` — Ruff E722
  - Do not use bare `except`

- **[medium] ruff / style** — `F:\Code-Quality-Agent\src\cq_agent\visualizations\trends.py:135` — Ruff F821
  - Undefined name `List`

- **[medium] ruff / style** — `F:\Code-Quality-Agent\src\cq_agent\visualizations\trends.py:135` — Ruff F821
  - Undefined name `Dict`

- **[medium] ruff / style** — `F:\Code-Quality-Agent\src\cq_agent\visualizations\trends.py:107` — Ruff F821
  - Undefined name `Dict`

- **[medium] ruff / style** — `F:\Code-Quality-Agent\src\cq_agent\visualizations\trends.py:104` — Ruff E722
  - Do not use bare `except`

- **[medium] ruff / style** — `F:\Code-Quality-Agent\src\cq_agent\visualizations\trends.py:64` — Ruff F821
  - Undefined name `Optional`

- **[medium] ruff / style** — `F:\Code-Quality-Agent\src\cq_agent\visualizations\trends.py:64` — Ruff F821
  - Undefined name `Dict`

- **[medium] ruff / style** — `F:\Code-Quality-Agent\src\cq_agent\visualizations\trends.py:60` — Ruff E722
  - Do not use bare `except`

- **[medium] ruff / style** — `F:\Code-Quality-Agent\src\cq_agent\visualizations\trends.py:54` — Ruff F821
  - Undefined name `List`

- **[medium] ruff / style** — `F:\Code-Quality-Agent\src\cq_agent\visualizations\trends.py:29` — Ruff F821
  - Undefined name `Dict`

- **[medium] ruff / style** — `F:\Code-Quality-Agent\src\cq_agent\visualizations\trends.py:26` — Ruff E722
  - Do not use bare `except`

- **[medium] ruff / style** — `F:\Code-Quality-Agent\src\cq_agent\visualizations\trends.py:11` — Ruff F401
  - `pathlib.Path` imported but unused

- **[medium] ruff / style** — `F:\Code-Quality-Agent\src\cq_agent\visualizations\dependency_graph.py:301` — Ruff F841
  - Local variable `graph` is assigned to but never used

- **[medium] ruff / style** — `F:\Code-Quality-Agent\src\cq_agent\visualizations\dependency_graph.py:297` — Ruff F821
  - Undefined name `Dict`

- **[medium] ruff / style** — `F:\Code-Quality-Agent\src\cq_agent\visualizations\dependency_graph.py:297` — Ruff F821
  - Undefined name `Tuple`

- **[medium] ruff / style** — `F:\Code-Quality-Agent\src\cq_agent\visualizations\dependency_graph.py:297` — Ruff F821
  - Undefined name `Dict`

- **[medium] ruff / style** — `F:\Code-Quality-Agent\src\cq_agent\visualizations\dependency_graph.py:286` — Ruff E722
  - Do not use bare `except`

- **[medium] ruff / style** — `F:\Code-Quality-Agent\src\cq_agent\visualizations\dependency_graph.py:258` — Ruff F821
  - Undefined name `Dict`

- **[medium] ruff / style** — `F:\Code-Quality-Agent\src\cq_agent\visualizations\dependency_graph.py:149` — Ruff E722
  - Do not use bare `except`

- **[medium] ruff / style** — `F:\Code-Quality-Agent\src\cq_agent\visualizations\dependency_graph.py:128` — Ruff F821
  - Undefined name `Dict`

- **[medium] ruff / style** — `F:\Code-Quality-Agent\src\cq_agent\visualizations\dependency_graph.py:122` — Ruff F821
  - Undefined name `Dict`

- **[medium] ruff / style** — `F:\Code-Quality-Agent\src\cq_agent\visualizations\dependency_graph.py:93` — Ruff E722
  - Do not use bare `except`

- **[medium] ruff / style** — `F:\Code-Quality-Agent\src\cq_agent\visualizations\dependency_graph.py:59` — Ruff F821
  - Undefined name `Dict`
