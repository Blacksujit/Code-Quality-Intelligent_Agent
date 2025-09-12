# Code Quality Report

Path: `F:\Code-Quality-Agent`


## Overview

- **files**: 15
- **SLOC**: 1255

## Hotspots (top 10)

- `src\cq_agent\ingestion\reader.py` — score: 0.31
- `src\cq_agent\web\app.py` — score: 0.30
- `src\cq_agent\analyzers\python_analyzers.py` — score: 0.27
- `src\cq_agent\analyzers\issue.py` — score: 0.27
- `src\cq_agent\analyzers\__init__.py` — score: 0.21
- `src\cq_agent\analyzers\js_analyzers.py` — score: 0.19
- `src\cq_agent\qa\index.py` — score: 0.14
- `src\cq_agent\cli\main.py` — score: 0.12
- `src\cq_agent\graph\deps.py` — score: 0.12
- `src\cq_agent\metrics\metrics.py` — score: 0.11

## Top Issues

- **[medium] heuristic-dup / duplication** — `src\cq_agent\cli\main.py:1` — Near-duplicate code across files
  - These files appear to share duplicated blocks: src\cq_agent\cli\main.py and src\cq_agent\web\app.py.
  - Suggested fix: Extract common code into a shared function/module.

- **[medium] ruff / style** — `F:\Code-Quality-Agent\src\cq_agent\web\app.py:23` — Ruff E402
  - Module level import not at top of file

- **[medium] ruff / style** — `F:\Code-Quality-Agent\src\cq_agent\web\app.py:22` — Ruff E402
  - Module level import not at top of file

- **[medium] ruff / style** — `F:\Code-Quality-Agent\src\cq_agent\web\app.py:21` — Ruff E402
  - Module level import not at top of file

- **[medium] ruff / style** — `F:\Code-Quality-Agent\src\cq_agent\web\app.py:20` — Ruff E402
  - Module level import not at top of file

- **[medium] ruff / style** — `F:\Code-Quality-Agent\src\cq_agent\web\app.py:19` — Ruff E402
  - Module level import not at top of file

- **[medium] ruff / style** — `F:\Code-Quality-Agent\src\cq_agent\web\app.py:18` — Ruff E402
  - Module level import not at top of file

- **[medium] ruff / style** — `F:\Code-Quality-Agent\src\cq_agent\web\app.py:17` — Ruff E402
  - Module level import not at top of file

- **[medium] ruff / style** — `F:\Code-Quality-Agent\src\cq_agent\web\app.py:15` — Ruff E402
  - Module level import not at top of file

- **[medium] ruff / style** — `F:\Code-Quality-Agent\src\cq_agent\web\app.py:14` — Ruff E402
  - Module level import not at top of file

- **[medium] ruff / style** — `F:\Code-Quality-Agent\src\cq_agent\web\app.py:5` — Ruff F401
  - `typing.Tuple` imported but unused

- **[medium] ruff / style** — `F:\Code-Quality-Agent\src\cq_agent\reporting\markdown.py:14` — Ruff F541
  - f-string without any placeholders

- **[medium] ruff / style** — `F:\Code-Quality-Agent\src\cq_agent\reporting\markdown.py:11` — Ruff F541
  - f-string without any placeholders

- **[medium] ruff / style** — `F:\Code-Quality-Agent\src\cq_agent\qa\index.py:93` — Ruff F841
  - Local variable `query_lower` is assigned to but never used

- **[medium] ruff / style** — `F:\Code-Quality-Agent\src\cq_agent\cli\main.py:4` — Ruff F401
  - `json` imported but unused

- **[medium] ruff / style** — `F:\Code-Quality-Agent\src\cq_agent\analyzers\issue.py:3` — Ruff F401
  - `typing.Optional` imported but unused

- **[low] heuristic-docs / docs** — `src\cq_agent\web\app.py:1` — Python module missing top-level docstring
  - Add a module docstring to explain purpose and usage.
  - Suggested fix: Add a brief module-level docstring.

- **[low] heuristic-docs / docs** — `src\cq_agent\scoring\score.py:1` — Python module missing top-level docstring
  - Add a module docstring to explain purpose and usage.
  - Suggested fix: Add a brief module-level docstring.

- **[low] heuristic-docs / docs** — `src\cq_agent\reporting\sarif.py:1` — Python module missing top-level docstring
  - Add a module docstring to explain purpose and usage.
  - Suggested fix: Add a brief module-level docstring.

- **[low] heuristic-docs / docs** — `src\cq_agent\reporting\markdown.py:1` — Python module missing top-level docstring
  - Add a module docstring to explain purpose and usage.
  - Suggested fix: Add a brief module-level docstring.

- **[low] heuristic-docs / docs** — `src\cq_agent\qa\index.py:1` — Python module missing top-level docstring
  - Add a module docstring to explain purpose and usage.
  - Suggested fix: Add a brief module-level docstring.

- **[low] heuristic-docs / docs** — `src\cq_agent\metrics\metrics.py:1` — Python module missing top-level docstring
  - Add a module docstring to explain purpose and usage.
  - Suggested fix: Add a brief module-level docstring.

- **[low] heuristic-docs / docs** — `src\cq_agent\ingestion\reader.py:1` — Python module missing top-level docstring
  - Add a module docstring to explain purpose and usage.
  - Suggested fix: Add a brief module-level docstring.

- **[low] heuristic-docs / docs** — `src\cq_agent\ingestion\__init__.py:1` — Python module missing top-level docstring
  - Add a module docstring to explain purpose and usage.
  - Suggested fix: Add a brief module-level docstring.

- **[low] heuristic-docs / docs** — `src\cq_agent\graph\deps.py:1` — Python module missing top-level docstring
  - Add a module docstring to explain purpose and usage.
  - Suggested fix: Add a brief module-level docstring.

- **[low] heuristic-docs / docs** — `src\cq_agent\cli\main.py:1` — Python module missing top-level docstring
  - Add a module docstring to explain purpose and usage.
  - Suggested fix: Add a brief module-level docstring.

- **[low] heuristic-docs / docs** — `src\cq_agent\autofix\auto.py:1` — Python module missing top-level docstring
  - Add a module docstring to explain purpose and usage.
  - Suggested fix: Add a brief module-level docstring.

- **[low] heuristic-docs / docs** — `src\cq_agent\analyzers\python_analyzers.py:1` — Python module missing top-level docstring
  - Add a module docstring to explain purpose and usage.
  - Suggested fix: Add a brief module-level docstring.

- **[low] heuristic-docs / docs** — `src\cq_agent\analyzers\js_analyzers.py:1` — Python module missing top-level docstring
  - Add a module docstring to explain purpose and usage.
  - Suggested fix: Add a brief module-level docstring.

- **[low] heuristic-docs / docs** — `src\cq_agent\analyzers\issue.py:1` — Python module missing top-level docstring
  - Add a module docstring to explain purpose and usage.
  - Suggested fix: Add a brief module-level docstring.

- **[low] heuristic-docs / docs** — `src\cq_agent\analyzers\__init__.py:1` — Python module missing top-level docstring
  - Add a module docstring to explain purpose and usage.
  - Suggested fix: Add a brief module-level docstring.
