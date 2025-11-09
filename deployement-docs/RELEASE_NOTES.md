## v0.1.0 — First Public MVP

Release date: 2025‑09‑14

### What’s new
- Streamlit UI with improved visualizations and real Git history trends
- Local LLM fallback when DeepSeek limits are hit (fast, offline)
- Robust deployment readiness for Streamlit Cloud and container flows

### Key improvements
- Trends charts now use accurate commit timestamps and 12‑hour time format
- Restored “red = added, green = removed” lines with clearer contrast
- Hover labels readable on dark/light themes; subtle chart borders
- Ultra‑robust import/path handling for Streamlit Cloud; simplified requirements
- README revamped with setup, usage, deployment options, and demo video section
- Added MIT LICENSE (2025)

### Install & run (quick)
```bash
pip install -r requirements.txt
streamlit run src/cq_agent/web/app.py
```

### CLI
```bash
cq-agent --help
cq-agent analyze . --autofix-dry-run
```

### Thanks
Huge thanks to early testers for feedback on visuals, dates, and deployment.


