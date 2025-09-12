# Code Quality Report

Path: `F:\Code-Quality-Agent`


## Overview

- **files**: 33
- **SLOC**: 7557

## Hotspots (top 10)

- `src\cq_agent\web\app.py` — score: 0.30
- `src\cq_agent\analyzers\issue.py` — score: 0.21
- `src\cq_agent\visualizations\advanced_deps.py` — score: 0.20
- `src\cq_agent\visualizations\__init__.py` — score: 0.20
- `src\cq_agent\analyzers\__init__.py` — score: 0.20
- `src\cq_agent\analyzers\python_analyzers.py` — score: 0.18
- `src\cq_agent\visualizations\trends.py` — score: 0.16
- `src\cq_agent\ingestion\reader.py` — score: 0.15
- `src\cq_agent\analyzers\js_analyzers.py` — score: 0.14
- `src\cq_agent\visualizations\hotspots.py` — score: 0.14

## Top Issues

- **[medium] heuristic-dup / duplication** — `src\cq_agent\visualizations\advanced_deps.py:1` — Near-duplicate code across files
  - These files appear to share duplicated blocks: src\cq_agent\visualizations\advanced_deps.py and src\cq_agent\visualizations\dependency_graph.py.
  - Suggested fix: Extract common code into a shared function/module.

- **[medium] ruff / style** — `F:\Code-Quality-Agent\src\cq_agent\web\app.py:43` — Ruff E402
  - Module level import not at top of file

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

- **[medium] ruff / style** — `F:\Code-Quality-Agent\src\cq_agent\web\app.py:33` — Ruff F401
  - `cq_agent.visualizations.dependency_graph.create_dependency_visualization` imported but unused

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

- **[medium] ruff / style** — `F:\Code-Quality-Agent\src\cq_agent\visualizations\trends.py:204` — Ruff F541
  - f-string without any placeholders

- **[medium] ruff / style** — `F:\Code-Quality-Agent\src\cq_agent\visualizations\trends.py:152` — Ruff F841
  - Local variable `languages` is assigned to but never used

- **[medium] ruff / style** — `F:\Code-Quality-Agent\src\cq_agent\visualizations\trends.py:151` — Ruff F841
  - Local variable `file_count` is assigned to but never used

- **[medium] ruff / style** — `F:\Code-Quality-Agent\src\cq_agent\visualizations\trends.py:150` — Ruff E722
  - Do not use bare `except`

- **[medium] ruff / style** — `F:\Code-Quality-Agent\src\cq_agent\visualizations\trends.py:105` — Ruff E722
  - Do not use bare `except`

- **[medium] ruff / style** — `F:\Code-Quality-Agent\src\cq_agent\visualizations\trends.py:61` — Ruff E722
  - Do not use bare `except`

- **[medium] ruff / style** — `F:\Code-Quality-Agent\src\cq_agent\visualizations\trends.py:27` — Ruff E722
  - Do not use bare `except`

- **[medium] ruff / style** — `F:\Code-Quality-Agent\src\cq_agent\visualizations\trends.py:12` — Ruff F401
  - `pathlib.Path` imported but unused

- **[medium] ruff / style** — `F:\Code-Quality-Agent\src\cq_agent\visualizations\trends.py:9` — Ruff F401
  - `typing.Tuple` imported but unused

- **[medium] ruff / style** — `F:\Code-Quality-Agent\src\cq_agent\visualizations\dependency_graph.py:302` — Ruff F841
  - Local variable `graph` is assigned to but never used

- **[medium] ruff / style** — `F:\Code-Quality-Agent\src\cq_agent\visualizations\dependency_graph.py:287` — Ruff E722
  - Do not use bare `except`

- **[medium] ruff / style** — `F:\Code-Quality-Agent\src\cq_agent\visualizations\dependency_graph.py:150` — Ruff E722
  - Do not use bare `except`

- **[medium] ruff / style** — `F:\Code-Quality-Agent\src\cq_agent\visualizations\dependency_graph.py:94` — Ruff E722
  - Do not use bare `except`

- **[medium] ruff / style** — `F:\Code-Quality-Agent\src\cq_agent\visualizations\dependency_graph.py:43` — Ruff F841
  - Local variable `content` is assigned to but never used

- **[medium] ruff / style** — `F:\Code-Quality-Agent\src\cq_agent\visualizations\dependency_graph.py:9` — Ruff F401
  - `pandas` imported but unused

- **[medium] ruff / style** — `F:\Code-Quality-Agent\src\cq_agent\visualizations\dependency_graph.py:8` — Ruff F401
  - `typing.List` imported but unused

- **[medium] ruff / style** — `F:\Code-Quality-Agent\src\cq_agent\visualizations\dependency_graph.py:8` — Ruff F401
  - `typing.Set` imported but unused

- **[medium] ruff / style** — `F:\Code-Quality-Agent\src\cq_agent\visualizations\advanced_deps.py:259` — Ruff E722
  - Do not use bare `except`

- **[medium] ruff / style** — `F:\Code-Quality-Agent\src\cq_agent\visualizations\advanced_deps.py:237` — Ruff E722
  - Do not use bare `except`

- **[medium] ruff / style** — `F:\Code-Quality-Agent\src\cq_agent\visualizations\advanced_deps.py:201` — Ruff E722
  - Do not use bare `except`

- **[medium] ruff / style** — `F:\Code-Quality-Agent\src\cq_agent\visualizations\advanced_deps.py:158` — Ruff E722
  - Do not use bare `except`

- **[medium] ruff / style** — `F:\Code-Quality-Agent\src\cq_agent\visualizations\advanced_deps.py:117` — Ruff E722
  - Do not use bare `except`

- **[medium] ruff / style** — `F:\Code-Quality-Agent\src\cq_agent\visualizations\advanced_deps.py:101` — Ruff E722
  - Do not use bare `except`

- **[medium] ruff / style** — `F:\Code-Quality-Agent\src\cq_agent\visualizations\advanced_deps.py:16` — Ruff F401
  - `math` imported but unused

- **[medium] ruff / style** — `F:\Code-Quality-Agent\src\cq_agent\visualizations\advanced_deps.py:11` — Ruff F401
  - `typing.List` imported but unused

- **[medium] ruff / style** — `F:\Code-Quality-Agent\src\cq_agent\visualizations\advanced_deps.py:11` — Ruff F401
  - `typing.Tuple` imported but unused
