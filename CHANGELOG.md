## v0.1.0 (2025-09-14)

### Highlights
- Fix trends visualizations: accurate commit timestamps, red/green lines for lines changed, improved hover visibility, better contrast.
- Robust Streamlit Cloud compatibility: resilient imports, path handling, and simplified requirements.
- Local LLM fallback in Streamlit UI and comprehensive README with setup, deployment, and demo section.
- Added MIT License and repository housekeeping.

### Changes
- Graphs/Trends: fixed date handling from Git history; restored visual styling; resolved array length mismatch; 12-hour time format.
- UI Styling: removed harsh white backgrounds; improved hover labels and borders; consistent theme across charts.
- Streamlit Deploy: added `setup.py`, simplified `requirements.txt`, resilient import strategy with dummy fallbacks, globals assignment for critical functions, path handling improvements.
- Docs: expanded `README.md` with examples, deployment options, local LLM instructions, and demo video guidance.
- Licensing: added MIT `LICENSE` (2025).

### Notable Commits
- Fix graph visibility and contrast issues
- Restore red/green lines visualization and fix hover visibility
- Fix timestamp accuracy in trends and visualizations
- Implement live analysis and resolve trend array length mismatch
- Implement robust import strategy for Streamlit Cloud
- Ensure TF‑IDF utilities and other functions are globally available
- Simplify requirements for Streamlit Cloud
- Add explanation video section to README
- Add LICENSE for the MVP


