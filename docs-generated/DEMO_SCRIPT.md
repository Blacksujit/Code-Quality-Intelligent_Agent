# Code Quality Intelligence Agent - Demo Script (5-7 minutes)

## Overview
This demo showcases our AI-powered Code Quality Intelligence Agent that analyzes multi-language codebases, identifies quality issues, and provides actionable insights with interactive Q&A.

## Demo Flow

### 1. Introduction (30 seconds)
- "I built a Code Quality Intelligence Agent for the Atlan AI Engineering internship challenge"
- "It analyzes Python and JavaScript/TypeScript codebases, finds quality issues, and provides interactive Q&A"
- "Let me show you the key features: CLI analysis, web UI, and intelligent code search"

### 2. CLI Analysis (2 minutes)
```bash
# Show the CLI in action
python -m cq_agent.cli.main analyze . --md demo-report.md --sarif demo-report.sarif

# Highlight the output:
# - Files: 15 | SLOC: 1255 | Languages: python
# - Issues found: 31 (shows top 10)
# - Generated reports

# Show autofix preview
python -m cq_agent.cli.main analyze . --autofix-dry-run
# - Shows unified diff of safe fixes (unused imports)
```

**Key points to mention:**
- Multi-language support (Python + JS/TS)
- Prioritized issues by severity and impact
- SARIF output for IDE/CI integration
- Safe autofix with dry-run preview

### 3. Web UI Demo (2.5 minutes)
```bash
# Launch the Streamlit UI
streamlit run src/cq_agent/web/app.py
```

**Show in UI:**
1. **Overview KPIs**: Files, SLOC, Languages, Issues count
2. **Dashboards tab**: 
   - Severity distribution bar chart
   - Top hotspots bar chart
3. **Issues tab**:
   - Filter by severity/category/source
   - Search functionality
   - Color-coded severity badges
4. **File Details tab**:
   - Select a file with issues
   - Show code context around issues
   - Expandable issue details
5. **Autofix tab**:
   - Preview safe fixes
   - Show confirmation flow
6. **Export tab**:
   - Download Markdown/CSV reports

**Key points:**
- Interactive filtering and search
- Visual dashboards with charts
- Per-file issue details with code context
- Safe autofix with confirmation
- Export capabilities

### 4. Q&A Demo (1.5 minutes)
```bash
# Start interactive Q&A
python -m cq_agent.cli.main qa .

# Ask questions like:
# - "How does the ingestion work?"
# - "What are the main analyzers?"
# - "Show me security issues"
# - "How is scoring implemented?"
```

**Key points:**
- Enhanced TF-IDF search with function/filename boosting
- File:line citations in results
- Natural language queries over codebase
- Relevant code snippets with context

### 5. Architecture & Technical Highlights (1 minute)
- **Modular design**: ingestion → analyzers → scoring → reporting
- **Smart prioritization**: git churn × complexity × centrality
- **Multi-analyzer**: Ruff, Bandit, Radon, ESLint
- **Hotspots detection**: dependency graph analysis
- **Safe autofix**: deterministic fixes with confirmation
- **CI/CD ready**: GitHub Action + SARIF integration

### 6. Conclusion (30 seconds)
- "This agent provides comprehensive code quality analysis with practical developer tools"
- "Key differentiators: smart prioritization, interactive UI, safe autofix, and intelligent Q&A"
- "Ready for production use with CI/CD integration and extensible architecture"

## Demo Tips
- Keep terminal and browser windows side by side
- Have sample outputs ready in `sample-outputs/`
- Practice the Q&A questions beforehand
- Show confidence in the technical decisions
- Emphasize practical developer value

## Backup Plan
If something fails:
- Show the sample outputs in `sample-outputs/`
- Explain the architecture from the notebook
- Highlight the GitHub Action workflow
- Discuss the modular, extensible design

## Key Messages
1. **Practical**: Solves real developer problems
2. **Intelligent**: Smart prioritization and search
3. **Safe**: Confirmation-based autofix
4. **Extensible**: Clean modular architecture
5. **Production-ready**: CI/CD integration
