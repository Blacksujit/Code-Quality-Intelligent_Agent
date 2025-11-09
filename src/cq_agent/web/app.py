from __future__ import annotations

import io
from pathlib import Path
import sys
from typing import List
# Ensure proper Python path for Streamlit Cloud deployment
_CURRENT = Path(__file__).resolve()

# Try multiple possible paths for different deployment scenarios
_possible_paths = [
    _CURRENT.parents[2],  # Go up from web/app.py -> cq_agent -> src
    _CURRENT.parent,      # cq_agent directory
    _CURRENT.parents[1],  # Go up from web/app.py -> cq_agent
    Path("/mount/src/code-quality-intelligent_agent/src"),  # Streamlit Cloud path
    Path("/mount/src/code-quality-intelligent_agent"),      # Streamlit Cloud root
]

for path in _possible_paths:
    if path.exists() and str(path) not in sys.path:
        sys.path.insert(0, str(path))

# Also add the current working directory
if str(Path.cwd()) not in sys.path:
    sys.path.insert(0, str(Path.cwd()))

import streamlit as st
import pandas as pd
import os
try:
    from dotenv import load_dotenv
    load_dotenv()
except Exception:
    pass

# Simple fallback import strategy
def _import_modules():
    """Import modules with simple fallback strategy"""
    # Try the most likely working imports first
    try:
        # Strategy 1: Try cq_agent imports
        from cq_agent.ingestion import load_repo
        from cq_agent.analyzers import analyze_python, analyze_js_ts, Issue
        from cq_agent.metrics.metrics import detect_near_duplicates, detect_docs_tests_hints
        from cq_agent.scoring.score import prioritize_issues
        from cq_agent.graph.deps import build_dependency_graph, compute_hotspots
        from cq_agent.reporting.markdown import build_markdown_text
        from cq_agent.autofix.auto import compute_autofixes, generate_patch, apply_edits
        
        return {
            'ingestion': type('Module', (), {'load_repo': load_repo}),
            'analyzers': type('Module', (), {'analyze_python': analyze_python, 'analyze_js_ts': analyze_js_ts, 'Issue': Issue}),
            'metrics': type('Module', (), {'detect_near_duplicates': detect_near_duplicates, 'detect_docs_tests_hints': detect_docs_tests_hints}),
            'scoring': type('Module', (), {'prioritize_issues': prioritize_issues}),
            'graph': type('Module', (), {'build_dependency_graph': build_dependency_graph, 'compute_hotspots': compute_hotspots}),
            'reporting': type('Module', (), {'build_markdown_text': build_markdown_text}),
            'autofix': type('Module', (), {'compute_autofixes': compute_autofixes, 'generate_patch': generate_patch, 'apply_edits': apply_edits})
        }
    except ImportError:
        pass
    
    # Strategy 2: Try direct imports
    try:
        from ingestion import load_repo
        from analyzers import analyze_python, analyze_js_ts, Issue
        from metrics.metrics import detect_near_duplicates, detect_docs_tests_hints
        from scoring.score import prioritize_issues
        from graph.deps import build_dependency_graph, compute_hotspots
        from reporting.markdown import build_markdown_text
        from autofix.auto import compute_autofixes, generate_patch, apply_edits
        
        return {
            'ingestion': type('Module', (), {'load_repo': load_repo}),
            'analyzers': type('Module', (), {'analyze_python': analyze_python, 'analyze_js_ts': analyze_js_ts, 'Issue': Issue}),
            'metrics': type('Module', (), {'detect_near_duplicates': detect_near_duplicates, 'detect_docs_tests_hints': detect_docs_tests_hints}),
            'scoring': type('Module', (), {'prioritize_issues': prioritize_issues}),
            'graph': type('Module', (), {'build_dependency_graph': build_dependency_graph, 'compute_hotspots': compute_hotspots}),
            'reporting': type('Module', (), {'build_markdown_text': build_markdown_text}),
            'autofix': type('Module', (), {'compute_autofixes': compute_autofixes, 'generate_patch': generate_patch, 'apply_edits': apply_edits})
        }
    except ImportError:
        pass
    
    # Strategy 3: Try absolute imports
    try:
        from src.cq_agent.ingestion import load_repo
        from src.cq_agent.analyzers import analyze_python, analyze_js_ts, Issue
        from src.cq_agent.metrics.metrics import detect_near_duplicates, detect_docs_tests_hints
        from src.cq_agent.scoring.score import prioritize_issues
        from src.cq_agent.graph.deps import build_dependency_graph, compute_hotspots
        from src.cq_agent.reporting.markdown import build_markdown_text
        from src.cq_agent.autofix.auto import compute_autofixes, generate_patch, apply_edits
        
        return {
            'ingestion': type('Module', (), {'load_repo': load_repo}),
            'analyzers': type('Module', (), {'analyze_python': analyze_python, 'analyze_js_ts': analyze_js_ts, 'Issue': Issue}),
            'metrics': type('Module', (), {'detect_near_duplicates': detect_near_duplicates, 'detect_docs_tests_hints': detect_docs_tests_hints}),
            'scoring': type('Module', (), {'prioritize_issues': prioritize_issues}),
            'graph': type('Module', (), {'build_dependency_graph': build_dependency_graph, 'compute_hotspots': compute_hotspots}),
            'reporting': type('Module', (), {'build_markdown_text': build_markdown_text}),
            'autofix': type('Module', (), {'compute_autofixes': compute_autofixes, 'generate_patch': generate_patch, 'apply_edits': apply_edits})
        }
    except ImportError:
        pass
    
    # If all fail, create dummy functions to prevent crashes
    def dummy_function(*args, **kwargs):
        return []
    
    def dummy_issue(*args, **kwargs):
        return type('Issue', (), {'file': '', 'line': 0, 'message': '', 'severity': 'low'})()
    
    return {
        'ingestion': type('Module', (), {'load_repo': dummy_function}),
        'analyzers': type('Module', (), {'analyze_python': dummy_function, 'analyze_js_ts': dummy_function, 'Issue': dummy_issue}),
        'metrics': type('Module', (), {'detect_near_duplicates': dummy_function, 'detect_docs_tests_hints': dummy_function}),
        'scoring': type('Module', (), {'prioritize_issues': dummy_function}),
        'graph': type('Module', (), {'build_dependency_graph': dummy_function, 'compute_hotspots': dummy_function}),
        'reporting': type('Module', (), {'build_markdown_text': dummy_function}),
        'autofix': type('Module', (), {'compute_autofixes': dummy_function, 'generate_patch': dummy_function, 'apply_edits': dummy_function})
    }

# Import the modules
_modules = _import_modules()

# Assign to global namespace
load_repo = _modules['ingestion'].load_repo
analyze_python = _modules['analyzers'].analyze_python
analyze_js_ts = _modules['analyzers'].analyze_js_ts
Issue = _modules['analyzers'].Issue
detect_near_duplicates = _modules['metrics'].detect_near_duplicates
detect_docs_tests_hints = _modules['metrics'].detect_docs_tests_hints
prioritize_issues = _modules['scoring'].prioritize_issues
build_dependency_graph = _modules['graph'].build_dependency_graph
compute_hotspots = _modules['graph'].compute_hotspots
build_markdown_text = _modules['reporting'].build_markdown_text
compute_autofixes = _modules['autofix'].compute_autofixes
generate_patch = _modules['autofix'].generate_patch
apply_edits = _modules['autofix'].apply_edits
# Simple fallback for remaining modules
def _import_remaining_modules():
    """Import remaining modules with simple fallback"""
    # Try different import strategies
    try:
        from cq_agent.web.components import (
            create_metrics_cards, create_severity_chart, create_hotspots_chart,
            create_trend_chart, create_language_distribution_chart, create_quality_score_gauge
        )
        from cq_agent.visualizations.advanced_deps import create_advanced_dependency_visualizations
        from cq_agent.visualizations.hotspots import create_hotspot_visualizations
        from cq_agent.visualizations.trends import create_trend_visualizations
        from cq_agent.agents.langgraph_trends import create_langgraph_trend_analysis
        from cq_agent.qa.index import build_index as build_tfidf_index
        from cq_agent.qa.index import save_index as save_tfidf_index
        from cq_agent.qa.index import load_index as load_tfidf_index
        from cq_agent.qa.index import _repo_head_key
        from cq_agent.analyzers.python_analyzers import run_ruff_on_files, run_bandit_on_paths
        from cq_agent.ai import enhance_issues_with_ai, answer_codebase_question
        try:
            from cq_agent.ai.agent_qa import run_agentic_qa
        except:
            run_agentic_qa = None
        
        # Make ALL imported functions available globally
        globals()['_repo_head_key'] = _repo_head_key
        globals()['build_tfidf_index'] = build_tfidf_index
        globals()['save_tfidf_index'] = save_tfidf_index
        globals()['load_tfidf_index'] = load_tfidf_index
        globals()['run_ruff_on_files'] = run_ruff_on_files
        globals()['run_bandit_on_paths'] = run_bandit_on_paths
        globals()['enhance_issues_with_ai'] = enhance_issues_with_ai
        globals()['answer_codebase_question'] = answer_codebase_question
        globals()['create_metrics_cards'] = create_metrics_cards
        globals()['create_severity_chart'] = create_severity_chart
        globals()['create_hotspots_chart'] = create_hotspots_chart
        globals()['create_trend_chart'] = create_trend_chart
        globals()['create_language_distribution_chart'] = create_language_distribution_chart
        globals()['create_quality_score_gauge'] = create_quality_score_gauge
        globals()['create_advanced_dependency_visualizations'] = create_advanced_dependency_visualizations
        globals()['create_hotspot_visualizations'] = create_hotspot_visualizations
        globals()['create_trend_visualizations'] = create_trend_visualizations
        globals()['create_langgraph_trend_analysis'] = create_langgraph_trend_analysis
        globals()['run_agentic_qa'] = run_agentic_qa
    except ImportError:
        try:
            from web.components import (
                create_metrics_cards, create_severity_chart, create_hotspots_chart,
                create_trend_chart, create_language_distribution_chart, create_quality_score_gauge
            )
            from visualizations.advanced_deps import create_advanced_dependency_visualizations
            from visualizations.hotspots import create_hotspot_visualizations
            from visualizations.trends import create_trend_visualizations
            from agents.langgraph_trends import create_langgraph_trend_analysis
            from qa.index import build_index as build_tfidf_index
            from qa.index import save_index as save_tfidf_index
            from qa.index import load_index as load_tfidf_index
            from qa.index import _repo_head_key
            from analyzers.python_analyzers import run_ruff_on_files, run_bandit_on_paths
            from ai import enhance_issues_with_ai, answer_codebase_question
            try:
                from ai.agent_qa import run_agentic_qa
            except:
                run_agentic_qa = None
            
            # Make ALL imported functions available globally
            globals()['_repo_head_key'] = _repo_head_key
            globals()['build_tfidf_index'] = build_tfidf_index
            globals()['save_tfidf_index'] = save_tfidf_index
            globals()['load_tfidf_index'] = load_tfidf_index
            globals()['run_ruff_on_files'] = run_ruff_on_files
            globals()['run_bandit_on_paths'] = run_bandit_on_paths
            globals()['enhance_issues_with_ai'] = enhance_issues_with_ai
            globals()['answer_codebase_question'] = answer_codebase_question
            globals()['create_metrics_cards'] = create_metrics_cards
            globals()['create_severity_chart'] = create_severity_chart
            globals()['create_hotspots_chart'] = create_hotspots_chart
            globals()['create_trend_chart'] = create_trend_chart
            globals()['create_language_distribution_chart'] = create_language_distribution_chart
            globals()['create_quality_score_gauge'] = create_quality_score_gauge
            globals()['create_advanced_dependency_visualizations'] = create_advanced_dependency_visualizations
            globals()['create_hotspot_visualizations'] = create_hotspot_visualizations
            globals()['create_trend_visualizations'] = create_trend_visualizations
            globals()['create_langgraph_trend_analysis'] = create_langgraph_trend_analysis
            globals()['run_agentic_qa'] = run_agentic_qa
        except ImportError:
            # Create dummy functions if all imports fail
            def dummy_function(*args, **kwargs):
                return []
            
            create_metrics_cards = dummy_function
            create_severity_chart = dummy_function
            create_hotspots_chart = dummy_function
            create_trend_chart = dummy_function
            create_language_distribution_chart = dummy_function
            create_quality_score_gauge = dummy_function
            create_advanced_dependency_visualizations = dummy_function
            create_hotspot_visualizations = dummy_function
            create_trend_visualizations = dummy_function
            create_langgraph_trend_analysis = dummy_function
            build_tfidf_index = dummy_function
            save_tfidf_index = dummy_function
            load_tfidf_index = dummy_function
            _repo_head_key = dummy_function
            run_ruff_on_files = dummy_function
            run_bandit_on_paths = dummy_function
            enhance_issues_with_ai = dummy_function
            answer_codebase_question = dummy_function
            run_agentic_qa = None
            
            # Make all functions available globally
            def _repo_head_key(repo):
                try:
                    return repo.head.commit.hexsha[:8]
                except:
                    return "unknown"
            
            globals()['_repo_head_key'] = _repo_head_key
            globals()['build_tfidf_index'] = dummy_function
            globals()['save_tfidf_index'] = dummy_function
            globals()['load_tfidf_index'] = dummy_function
            globals()['run_ruff_on_files'] = dummy_function
            globals()['run_bandit_on_paths'] = dummy_function
            globals()['enhance_issues_with_ai'] = dummy_function
            globals()['answer_codebase_question'] = dummy_function
            globals()['create_metrics_cards'] = dummy_function
            globals()['create_severity_chart'] = dummy_function
            globals()['create_hotspots_chart'] = dummy_function
            globals()['create_trend_chart'] = dummy_function
            globals()['create_language_distribution_chart'] = dummy_function
            globals()['create_quality_score_gauge'] = dummy_function
            globals()['create_advanced_dependency_visualizations'] = dummy_function
            globals()['create_hotspot_visualizations'] = dummy_function
            globals()['create_trend_visualizations'] = dummy_function
            globals()['create_langgraph_trend_analysis'] = dummy_function
            globals()['run_agentic_qa'] = None

# Import the remaining modules
_import_remaining_modules()

# Ensure _repo_head_key is available globally
if '_repo_head_key' not in globals():
    def _repo_head_key(repo):
        """Fallback function for _repo_head_key"""
        try:
            # Try to get git commit hash
            if hasattr(repo, 'head') and hasattr(repo.head, 'commit'):
                return repo.head.commit.hexsha[:8]
            # Try alternative: check if repo has git info
            if isinstance(repo, dict) and 'git' in repo:
                git_info = repo.get('git', {})
                if isinstance(git_info, dict) and 'head' in git_info:
                    return str(git_info['head'])[:8]
            # Fallback to hash of repo path or timestamp
            import hashlib
            repo_str = str(repo) if not isinstance(repo, dict) else str(repo.get('root', 'unknown'))
            return hashlib.md5(repo_str.encode()).hexdigest()[:8]
        except Exception:
            return "unknown"


# Helper: render a widget safely so one error doesn't break the whole page
def _safe_render(label: str, renderer, *args, **kwargs):
    try:
        return renderer(*args, **kwargs)
    except Exception as exc:
        st.error(f"Failed to render {label}: {exc}")
        return None


st.set_page_config(
	page_title="Code Quality Intelligence Agent", 
	layout="wide",
	initial_sidebar_state="expanded",
	page_icon="🔍"
)

# Production-grade CSS with modern design
st.markdown(
	"""
	<style>
	/* Import Google Fonts */
	@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
	@import url('https://fonts.googleapis.com/css2?family=Fira+Code:wght@300;400;500;600;700&display=swap');
	
	/* Global Styles - Glassmorphism Design */
	.main .block-container { padding-top: 1rem; padding-bottom: 1rem; }
	.stApp { 
		background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
		min-height: 100vh;
	}
	.main .block-container { 
		background: rgba(255, 255, 255, 0.1); 
		backdrop-filter: blur(20px);
		border: 1px solid rgba(255, 255, 255, 0.2);
		border-radius: 20px; 
		box-shadow: 0 20px 40px rgba(0,0,0,0.1);
	}
	
	/* Glassmorphism Cards */
	.glass-card {
		background: rgba(255, 255, 255, 0.15);
		backdrop-filter: blur(10px);
		border: 1px solid rgba(255, 255, 255, 0.2);
		border-radius: 15px;
		padding: 1.5rem;
		box-shadow: 0 8px 32px rgba(0,0,0,0.1);
		transition: all 0.3s ease;
	}
	.glass-card:hover {
		background: rgba(255, 255, 255, 0.2);
		transform: translateY(-2px);
		box-shadow: 0 12px 40px rgba(0,0,0,0.15);
	}
	
	/* Adaptive Text Colors */
	h1, h2, h3, h4, h5, h6 { 
		color: #ffffff !important; 
		font-weight: 600 !important; 
		text-shadow: 0 2px 4px rgba(0,0,0,0.3);
	}
	.stMarkdown h1, .stMarkdown h2, .stMarkdown h3, .stMarkdown h4, .stMarkdown h5, .stMarkdown h6 { 
		color: #ffffff !important; 
		text-shadow: 0 2px 4px rgba(0,0,0,0.3);
	}
	
	/* Base text colors for readability */
	.stMarkdown, .stMarkdown p, .stMarkdown li, .stMarkdown span, p, li, span { 
		color: rgba(255, 255, 255, 0.9) !important; 
	}
	label, .stTextInput label, .stNumberInput label, .stSelectbox label, .stMultiselect label { 
		color: rgba(255, 255, 255, 0.9) !important; 
		font-weight: 500;
	}

	/* Sidebar Glassmorphism */
	.css-1d391kg, .sidebar .sidebar-content { 
		background: rgba(255, 255, 255, 0.1) !important; 
		backdrop-filter: blur(20px);
		border-right: 1px solid rgba(255, 255, 255, 0.2);
	}
	.sidebar .stMarkdown, .sidebar p, .sidebar label, .sidebar span { 
		color: rgba(255, 255, 255, 0.9) !important; 
	}
	
	/* Header */
	.main-header { 
		text-align: center; 
		margin-bottom: 2rem; 
		padding: 2rem 0;
		background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
		border-radius: 15px;
		color: white;
		box-shadow: 0 10px 30px rgba(0,0,0,0.2);
	}
	.main-header h1 { 
		font-family: 'Inter', sans-serif; 
		font-weight: 700; 
		font-size: 2.5rem; 
		margin: 0;
		text-shadow: 0 2px 4px rgba(0,0,0,0.3);
	}
	.main-header p { 
		font-family: 'Inter', sans-serif; 
		font-size: 1.1rem; 
		margin: 0.5rem 0 0 0;
		opacity: 0.9;
	}
	
	/* Metrics Cards - Glassmorphism */
	.metric-card { 
		background: rgba(255, 255, 255, 0.15);
		backdrop-filter: blur(10px);
		border: 1px solid rgba(255, 255, 255, 0.2);
		padding: 1.5rem; 
		border-radius: 15px; 
		box-shadow: 0 8px 32px rgba(0,0,0,0.1);
		border-left: 4px solid rgba(255, 255, 255, 0.4);
		transition: all 0.3s ease;
	}
	.metric-card:hover { 
		background: rgba(255, 255, 255, 0.2);
		transform: translateY(-2px); 
		box-shadow: 0 12px 40px rgba(0,0,0,0.15);
	}
	.metric-value { 
		font-family: 'Inter', sans-serif; 
		font-weight: 700; 
		font-size: 2rem; 
		color: #ffffff; 
		margin: 0;
		text-shadow: 0 2px 4px rgba(0,0,0,0.3);
	}
	.metric-label { 
		font-family: 'Inter', sans-serif; 
		font-size: 0.9rem; 
		color: rgba(255, 255, 255, 0.8); 
		margin: 0;
		text-transform: uppercase;
		letter-spacing: 0.5px;
	}
	
	/* Badges */
	.badge { 
		padding: 4px 12px; 
		border-radius: 20px; 
		font-size: 11px; 
		font-weight: 600;
		color: white; 
		text-transform: uppercase;
		letter-spacing: 0.5px;
		box-shadow: 0 2px 4px rgba(0,0,0,0.1);
	}
	.badge-critical { background: linear-gradient(135deg, #e74c3c, #c0392b); }
	.badge-high { background: linear-gradient(135deg, #f39c12, #e67e22); }
	.badge-medium { background: linear-gradient(135deg, #f1c40f, #f39c12); color: #2c3e50; }
	.badge-low { background: linear-gradient(135deg, #27ae60, #2ecc71); }
	
	/* Sidebar - Glassmorphism */
	.css-1d391kg { 
		background: rgba(255, 255, 255, 0.1) !important; 
		backdrop-filter: blur(20px);
		border-right: 1px solid rgba(255, 255, 255, 0.2);
	}
	.sidebar .sidebar-content { 
		background: rgba(255, 255, 255, 0.1) !important; 
		backdrop-filter: blur(20px);
	}
	
	/* Buttons - Glassmorphism */
	.stButton > button { 
		background: rgba(255, 255, 255, 0.2);
		backdrop-filter: blur(10px);
		border: 1px solid rgba(255, 255, 255, 0.3);
		color: white;
		border-radius: 10px;
		padding: 0.5rem 1.5rem;
		font-weight: 600;
		transition: all 0.3s ease;
		box-shadow: 0 4px 15px rgba(255, 255, 255, 0.1);
	}
	.stButton > button:hover { 
		background: rgba(255, 255, 255, 0.3);
		transform: translateY(-2px); 
		box-shadow: 0 6px 20px rgba(255, 255, 255, 0.2);
	}
	
	/* Input Elements - Glassmorphism */
	.stTextInput > div > div > input,
	.stNumberInput > div > div > input,
	.stSelectbox > div > div > div,
	.stMultiselect > div > div > div {
		background: rgba(255, 255, 255, 0.1) !important;
		backdrop-filter: blur(10px);
		border: 1px solid rgba(255, 255, 255, 0.2) !important;
		border-radius: 8px !important;
		color: rgba(255, 255, 255, 0.9) !important;
	}
	.stTextInput > div > div > input:focus,
	.stNumberInput > div > div > input:focus {
		border-color: rgba(255, 255, 255, 0.4) !important;
		box-shadow: 0 0 0 2px rgba(255, 255, 255, 0.1) !important;
	}
	
	/* Tabs - Glassmorphism */
	.stTabs [data-baseweb="tab-list"] { 
		gap: 8px; 
		background: rgba(255, 255, 255, 0.1);
		backdrop-filter: blur(10px);
		border: 1px solid rgba(255, 255, 255, 0.2);
		padding: 8px;
		border-radius: 15px;
	}
	.stTabs [data-baseweb="tab"] { 
		background: rgba(255, 255, 255, 0.1); 
		backdrop-filter: blur(5px);
		border: 1px solid rgba(255, 255, 255, 0.1);
		border-radius: 10px; 
		padding: 0.5rem 1rem;
		font-weight: 600;
		color: rgba(255, 255, 255, 0.8);
		transition: all 0.3s ease;
	}
	.stTabs [aria-selected="true"] { 
		background: rgba(255, 255, 255, 0.2);
		backdrop-filter: blur(10px);
		border: 1px solid rgba(255, 255, 255, 0.3);
		color: white;
		box-shadow: 0 4px 15px rgba(255, 255, 255, 0.2);
	}
	
	/* Data Tables - Glassmorphism */
	.stDataFrame { 
		border-radius: 15px; 
		overflow: hidden;
		background: rgba(255, 255, 255, 0.1) !important;
		backdrop-filter: blur(10px);
		border: 1px solid rgba(255, 255, 255, 0.2);
		color: rgba(255, 255, 255, 0.9) !important;
		box-shadow: 0 8px 32px rgba(0,0,0,0.1);
	}
	/* Generic table container for HTML-rendered tables */
	.table-container { 
		background: rgba(255, 255, 255, 0.1); 
		backdrop-filter: blur(10px);
		border: 1px solid rgba(255, 255, 255, 0.2);
		border-radius: 12px; 
		padding: 8px; 
		box-shadow: 0 8px 32px rgba(0,0,0,0.1);
	}
	.table-container table { 
		width: 100%; 
		color: rgba(255, 255, 255, 0.9); 
		border-collapse: collapse; 
	}
	.table-container th { 
		background: rgba(255, 255, 255, 0.15); 
		color: rgba(255, 255, 255, 0.9); 
		padding: 8px; 
		text-align: left; 
		font-weight: 600;
	}
	.table-container td { 
		color: rgba(255, 255, 255, 0.8); 
		padding: 8px; 
		border-top: 1px solid rgba(255, 255, 255, 0.1); 
	}

	/* Links */
	a { color: #3b82f6; }
	
	/* Code Blocks - Developer Style */
	.stCode { 
		border-radius: 10px; 
		box-shadow: 0 8px 32px rgba(0,0,0,0.2);
		background: rgba(0, 0, 0, 0.8) !important;
		backdrop-filter: blur(10px);
		border: 1px solid rgba(255, 255, 255, 0.1);
	}
	.stCode pre, code { 
		color: #e6e6e6 !important; 
		background: rgba(0, 0, 0, 0.8) !important; 
		font-family: 'Fira Code', 'Monaco', 'Consolas', monospace !important;
		font-size: 0.9rem;
		line-height: 1.5;
	}
	
	/* Syntax highlighting for code snippets */
	.code-snippet {
		background: rgba(0, 0, 0, 0.8);
		backdrop-filter: blur(10px);
		border: 1px solid rgba(255, 255, 255, 0.1);
		border-radius: 8px;
		padding: 1rem;
		margin: 0.5rem 0;
		font-family: 'Fira Code', 'Monaco', 'Consolas', monospace;
		font-size: 0.85rem;
		line-height: 1.4;
		color: #e6e6e6;
		overflow-x: auto;
		box-shadow: 0 4px 20px rgba(0,0,0,0.3);
	}
	.code-snippet .line-number {
		color: #666;
		user-select: none;
		margin-right: 1rem;
	}
	.code-snippet .highlight-line {
		background: rgba(255, 255, 0, 0.1);
		border-left: 3px solid #ffd700;
		padding-left: 0.5rem;
	}
	
	/* Success/Error Messages */
	.stSuccess { 
		background: linear-gradient(135deg, #27ae60, #2ecc71);
		color: white;
		border-radius: 10px;
		padding: 1rem;
		box-shadow: 0 4px 15px rgba(39, 174, 96, 0.3);
	}
	.stError { 
		background: linear-gradient(135deg, #e74c3c, #c0392b);
		color: white;
		border-radius: 10px;
		padding: 1rem;
		box-shadow: 0 4px 15px rgba(231, 76, 60, 0.3);
	}
	
	/* Loading Spinner */
	.stSpinner { color: #667eea; }
	
	/* File Details - Glassmorphism */
	.file-detail-card {
		background: rgba(255, 255, 255, 0.15);
		backdrop-filter: blur(10px);
		border: 1px solid rgba(255, 255, 255, 0.2);
		border-radius: 15px;
		padding: 1.5rem;
		margin: 1rem 0;
		box-shadow: 0 8px 32px rgba(0,0,0,0.1);
		border-left: 4px solid rgba(255, 255, 255, 0.4);
		transition: all 0.3s ease;
	}
	.file-detail-card:hover {
		background: rgba(255, 255, 255, 0.2);
		transform: translateY(-2px);
		box-shadow: 0 12px 40px rgba(0,0,0,0.15);
	}
	.file-detail-card h4 {
		color: #ffffff !important;
		text-shadow: 0 2px 4px rgba(0,0,0,0.3);
	}
	.file-detail-card p {
		color: rgba(255, 255, 255, 0.8) !important;
	}
	
	/* Animations */
	@keyframes fadeInUp {
		from { opacity: 0; transform: translateY(20px); }
		to { opacity: 1; transform: translateY(0); }
	}
	.fade-in-up { animation: fadeInUp 0.6s ease-out; }
	
	/* Responsive */
	@media (max-width: 768px) {
		.main-header h1 { font-size: 2rem; }
		.metric-value { font-size: 1.5rem; }
	}
	</style>
	""",
	unsafe_allow_html=True,
)

# Modern Header with gradient background
st.markdown(
	"""
	<div class="main-header fade-in-up">
		<h1>🔍 Code Quality Intelligence Agent</h1>
		<p>AI-powered code analysis with smart prioritization and interactive insights</p>
	</div>
	""",
	unsafe_allow_html=True,
)

# Session state keys: repo_summary, issues_df, hotspots_df, root
if "repo_summary" not in st.session_state:
	st.session_state.repo_summary = None
if "issues_df" not in st.session_state:
	st.session_state.issues_df = None
if "hotspots_df" not in st.session_state:
	st.session_state.hotspots_df = None
if "root" not in st.session_state:
	st.session_state.root = None

# Enhanced Sidebar with modern design
with st.sidebar:
	st.markdown(
		"""
		<div style="text-align: center; margin-bottom: 2rem;">
			<h2 style="color: #2c3e50; font-family: 'Inter', sans-serif; font-weight: 600;">⚙️ Analysis Controls</h2>
		</div>
		""",
		unsafe_allow_html=True,
	)
	
	default_path = str(Path.cwd())
	path = st.text_input(
		"📁 Repository Path", 
		value=default_path, 
		help="Enter the path to your code repository (single path only, no spaces or multiple paths)"
	)
	
	# Clean the path input immediately
	if path:
		path = path.strip()
	max_files = st.number_input("📊 Max Files to Scan", min_value=50, max_value=10000, value=2000, step=50, help="Limit files for faster analysis on large repos")
	fast_mode = st.checkbox("⚡ Fast scan (large repos)", value=True, help="Skips heavy linters and samples files to speed up very large codebases")
	clear_cache_btn = st.button("🧹 Clear Analysis Cache", use_container_width=True)
	
	st.markdown("---")
	
	# AI Configuration (DeepSeek + Local Fallback)
	st.markdown("### 🤖 AI Configuration")
	_env_key = os.getenv("DEEPSEEK_API_KEY", "")
	has_api_key = bool(_env_key)
	
	# AI Backend Selection
	ai_backend = st.selectbox(
		"🧠 AI Backend",
		["DeepSeek (Remote)", "Local LLM (Fast)", "Disabled"],
		index=0 if has_api_key else 2,
		help="Choose AI backend for Q&A and issue enhancement"
	)
	
	use_deepseek = (ai_backend == "DeepSeek (Remote)" and has_api_key)
	use_local_llm = (ai_backend == "Local LLM (Fast)")
	
	if use_deepseek:
		st.success("✅ DeepSeek AI is configured and ready!")
	elif use_local_llm:
		st.info("🏠 Local LLM: Fast, offline, no API keys required")
		if run_agentic_qa is None:
			st.warning("⚠️ Local LLM support not available. Install: pip install transformers torch")
			use_local_llm = False
	else:
		st.info("ℹ️ AI features disabled. Enable DeepSeek or Local LLM for AI-powered Q&A")
	
	st.session_state.use_deepseek = use_deepseek
	st.session_state.use_local_llm = use_local_llm
	st.session_state.deepseek_api_key = _env_key
	
	st.markdown("---")
	
	run_clicked = st.button("🚀 Run Analysis", type="primary", use_container_width=True)
	
	st.markdown("---")
	
	# Quick stats if analysis is done
	if st.session_state.repo_summary is not None:
		st.markdown("### 📈 Quick Stats")
		summary = st.session_state.repo_summary
		st.metric("Files", summary.get("file_count", 0))
		st.metric("SLOC", summary.get("sloc_total", 0))
		st.metric("Languages", len(summary.get("languages", [])))
	
	st.markdown("---")
	st.markdown(
		"""
		<div style="text-align: center; color: #7f8c8d; font-size: 0.8rem;">
			💡 <strong>Pro Tip:</strong> Use smaller file caps for faster scans on huge repos
		</div>
		""",
		unsafe_allow_html=True,
	)

# Analysis function cached to avoid recomputation on rerun
@st.cache_data(show_spinner=False)
def run_analysis_cached(path_str: str, max_files_int: int, fast: bool):
		# Clean and validate path input (same logic as streaming function)
		path_str = path_str.strip()
		if ' ' in path_str:
			parts = path_str.split()
			valid_path = None
			for part in parts:
				part = part.strip()
				if part:
					test_path = Path(part).expanduser()
					if test_path.exists():
						valid_path = part
						break
					if len(part) >= 2 and part[1] == ':' and part[0].isalpha():
						valid_path = part
						break
			if valid_path:
				path_str = valid_path
			else:
				path_str = parts[0].strip() if parts else path_str
		
		root = Path(path_str).expanduser().resolve()
		if not root.exists():
			raise FileNotFoundError(f"Path not found: {root}")
		
		# In fast mode, cap files and skip heavy external linters
		effective_max = int(max_files_int)
		if fast:
			# Smaller cap and early return for responsiveness on huge repos
			effective_max = min(effective_max, 800)
		repo = load_repo(str(root), max_files=effective_max)

		issues: list[Issue] = []
		if not fast:
			if "python" in repo["languages"]:
				issues.extend(analyze_python(root))
			if any(lang in repo["languages"] for lang in ("javascript", "typescript")):
				issues.extend(analyze_js_ts(root))
		# Lightweight heuristics always
		issues.extend(detect_near_duplicates(repo))
		issues.extend(detect_docs_tests_hints(repo))
		if issues:
			issues = prioritize_issues(issues)

		# Build graph early for centrality
		graph = build_dependency_graph(repo)
		hotspots = compute_hotspots(repo, graph)

		# Fast mode: targeted linting using priority sampling and cached TF-IDF index
		if fast:
			# Build/load TF-IDF index cache (only if functions are available)
			if 'load_tfidf_index' in globals() and 'build_tfidf_index' in globals() and 'save_tfidf_index' in globals():
				try:
					cache_dir = Path.home() / ".cq_agent_cache"
					key = _repo_head_key(repo) if '_repo_head_key' in globals() else "default"
					index = load_tfidf_index(cache_dir, key)
					if index is None:
						index = build_tfidf_index(repo, max_files=1200)
						save_tfidf_index(index, cache_dir, key)
				except Exception:
					# If TF-IDF indexing fails, continue without it
					index = None

			# Priority sampling: churn, simple degree (in+out) on dict-graph, SLOC
			from collections import defaultdict as _dd
			in_degree: dict[str, int] = _dd(int)
			for src, deps in graph.items():
				for dst in deps:
					in_degree[dst] += 1
			file_scores: dict[str, float] = {}
			churn = repo.get("git", {}).get("churn_by_file", {}) if isinstance(repo.get("git", {}), dict) else {}
			for f, rec in repo.get("files", {}).items():
				out_deg = len(graph.get(f, set()))
				deg = int(out_deg) + int(in_degree.get(f, 0))
				sloc = rec.get("sloc", 0)
				ch = churn.get(f, 0)
				file_scores[f] = 0.5 * deg + 0.3 * (sloc ** 0.5) + 0.2 * ch
			# Select top-N files within budget
			budget = min(200, max(50, int(effective_max * 0.25)))
			priority_files = [f for f, _ in sorted(file_scores.items(), key=lambda x: x[1], reverse=True)[:budget]]

			# Targeted Python security/style (only if functions are available)
			py_files = [f for f in priority_files if f.endswith(".py")]
			if py_files:
				try:
					if 'run_ruff_on_files' in globals():
						issues.extend(run_ruff_on_files(root, py_files))
					if 'run_bandit_on_paths' in globals():
						issues.extend(run_bandit_on_paths(root, py_files))
				except Exception:
					# If linting fails, continue without it
					pass
				if issues:
					issues = prioritize_issues(issues)
		return root, repo, issues, hotspots

# Streaming analysis with progress updates
def run_analysis_streaming(path_str: str, max_files_int: int, fast: bool, use_deepseek: bool = False, use_local_llm: bool = False):
	"""Run analysis with progress streaming and partial result updates."""
	# Clean and validate path input
	# Remove leading/trailing whitespace and handle cases where multiple paths might be entered
	path_str = path_str.strip()
	
	# If path contains spaces and looks like multiple paths, take the first valid one
	# or the one that looks like an absolute path
	if ' ' in path_str:
		# Split by space and find the first valid path
		parts = path_str.split()
		valid_path = None
		valid_path_found = False
		
		# First pass: find any path that actually exists
		for part in parts:
			part = part.strip()
			if part:
				test_path = Path(part).expanduser().resolve()
				if test_path.exists():
					valid_path = part
					valid_path_found = True
					break
		
		# Second pass: if no existing path, look for absolute Windows paths
		if not valid_path_found:
			for part in parts:
				part = part.strip()
				if part and len(part) >= 2 and part[1] == ':' and part[0].isalpha():
					valid_path = part
					break
		
		if valid_path:
			path_str = valid_path
		else:
			# If no valid path found, use the first part
			path_str = parts[0].strip() if parts else path_str
	
	root = Path(path_str).expanduser().resolve()
	
	# Validate path exists before proceeding
	if not root.exists():
		raise FileNotFoundError(
			f"Path not found: {root}\n\n"
			f"Please check:\n"
			f"1. The path is correct: {path_str}\n"
			f"2. The directory exists\n"
			f"3. You have read permissions\n"
			f"4. Remove any extra spaces or multiple paths"
		)
	
	effective_max = int(max_files_int)
	if fast:
		effective_max = min(effective_max, 800)
	
	# Progress tracking
	progress_bar = st.progress(0)
	status_text = st.empty()
	
	# Step 1: Repository ingestion
	status_text.text("📁 Loading repository...")
	progress_bar.progress(10)
	repo = load_repo(str(root), max_files=effective_max)
	
	# Step 2: Basic analysis
	status_text.text("🔍 Running code analysis...")
	progress_bar.progress(30)
	issues: list[Issue] = []
	if not fast:
		if "python" in repo["languages"]:
			issues.extend(analyze_python(root))
		if any(lang in repo["languages"] for lang in ("javascript", "typescript")):
			issues.extend(analyze_js_ts(root))
	
	# Step 3: Heuristics and prioritization
	status_text.text("🧠 Computing heuristics...")
	progress_bar.progress(50)
	issues.extend(detect_near_duplicates(repo))
	issues.extend(detect_docs_tests_hints(repo))
	if issues:
		issues = prioritize_issues(issues)
	
	# Step 4: Graph analysis
	status_text.text("📊 Building dependency graph...")
	progress_bar.progress(70)
	graph = build_dependency_graph(repo)
	hotspots = compute_hotspots(repo, graph)
	
	# Step 5: Fast mode enhancements
	if fast:
		status_text.text("⚡ Fast mode: Priority sampling...")
		progress_bar.progress(85)
		# Fast mode logic (same as cached version) - only if functions are available
		if 'load_tfidf_index' in globals() and 'build_tfidf_index' in globals() and 'save_tfidf_index' in globals():
			try:
				cache_dir = Path.home() / ".cq_agent_cache"
				key = _repo_head_key(repo) if '_repo_head_key' in globals() else "default"
				index = load_tfidf_index(cache_dir, key)
				if index is None:
					index = build_tfidf_index(repo, max_files=1200)
					save_tfidf_index(index, cache_dir, key)
			except Exception:
				# If TF-IDF indexing fails, continue without it
				index = None
		
		from collections import defaultdict as _dd
		in_degree: dict[str, int] = _dd(int)
		for src, deps in graph.items():
			for dst in deps:
				in_degree[dst] += 1
		file_scores: dict[str, float] = {}
		churn = repo.get("git", {}).get("churn_by_file", {}) if isinstance(repo.get("git", {}), dict) else {}
		for f, rec in repo.get("files", {}).items():
			out_deg = len(graph.get(f, set()))
			deg = int(out_deg) + int(in_degree.get(f, 0))
			sloc = rec.get("sloc", 0)
			ch = churn.get(f, 0)
			file_scores[f] = 0.5 * deg + 0.3 * (sloc ** 0.5) + 0.2 * ch
		budget = min(200, max(50, int(effective_max * 0.25)))
		priority_files = [f for f, _ in sorted(file_scores.items(), key=lambda x: x[1], reverse=True)[:budget]]
		py_files = [f for f in priority_files if f.endswith(".py")]
		if py_files:
			try:
				if 'run_ruff_on_files' in globals():
					issues.extend(run_ruff_on_files(root, py_files))
				if 'run_bandit_on_paths' in globals():
					issues.extend(run_bandit_on_paths(root, py_files))
			except Exception:
				# If linting fails, continue without it
				pass
			if issues:
				issues = prioritize_issues(issues)
	
	# Step 6: AI enhancement (if enabled)
	if use_deepseek and st.session_state.get("deepseek_api_key"):
		status_text.text("🤖 Enhancing with DeepSeek AI...")
		progress_bar.progress(95)
		try:
			if 'enhance_issues_with_ai' in globals() and callable(globals()['enhance_issues_with_ai']):
				issues = enhance_issues_with_ai(issues, repo, st.session_state.deepseek_api_key)
			else:
				st.warning("⚠️ AI enhancement not available")
		except Exception as e:
			st.warning(f"⚠️ AI enhancement failed: {e}")
	elif use_local_llm and 'run_agentic_qa' in globals() and run_agentic_qa is not None:
		status_text.text("🏠 Enhancing with Local LLM...")
		progress_bar.progress(95)
		try:
			# Use local LLM for issue enhancement (simplified)
			enhanced_issues = []
			for issue in issues[:10]:  # Limit to top 10 for speed
				try:
					question = f"Analyze this {issue.get('source', 'code')} issue: {issue.get('title', '')}"
					answer, _ = run_agentic_qa(question, repo, backend="local", model="microsoft/DialoGPT-small")
					if answer and not answer.startswith("Extractive summary"):
						issue = issue.copy()
						issue['ai_justification'] = answer[:200] + "..." if len(answer) > 200 else answer
						issue['ai_severity'] = issue.get('severity', 'medium')
				except Exception:
					pass
				enhanced_issues.append(issue)
			issues = enhanced_issues + issues[10:]  # Keep rest unchanged
		except Exception as e:
			st.warning(f"⚠️ Local LLM enhancement failed: {e}")
	
	# Complete
	status_text.text("✅ Analysis complete!")
	progress_bar.progress(100)
	
	# Clear progress indicators
	progress_bar.empty()
	status_text.empty()
	
	return root, repo, issues, hotspots

# Trigger analysis
if clear_cache_btn:
	try:
		run_analysis_cached.clear()
		st.success("Cache cleared. Re-run analysis.")
	except Exception:
		st.info("Cache already clear.")

if run_clicked:
	# Clean path one more time before using (defensive programming)
	clean_path = path.strip() if path else ""
	
	# If path contains spaces, try to extract valid path
	if ' ' in clean_path:
		parts = clean_path.split()
		valid_path_found = False
		# First, try to find a path that actually exists
		for part in parts:
			part = part.strip()
			if part:
				test_path = Path(part).expanduser().resolve()
				if test_path.exists():
					clean_path = part
					valid_path_found = True
					break
		
		# If no existing path found, look for absolute Windows paths (drive letter format)
		if not valid_path_found:
			for part in parts:
				part = part.strip()
				if part and len(part) >= 2 and part[1] == ':' and part[0].isalpha():
					clean_path = part
					break
		
		# If still no valid path, use first part
		if not valid_path_found and len(parts) > 0:
			clean_path = parts[0].strip()
	
	# Validate path exists before calling analysis
	if not clean_path:
		st.error("❌ Please enter a repository path")
		st.stop()
	
	test_root = Path(clean_path).expanduser().resolve()
	if not test_root.exists():
		st.error(f"❌ Path not found: {clean_path}\n\nPlease check:\n1. The path is correct\n2. The directory exists\n3. Remove any extra spaces or multiple paths")
		st.stop()
	
	# Use streaming analysis for better UX
	try:
		root, repo, issues, hotspots = run_analysis_streaming(
			clean_path, int(max_files), bool(fast_mode), 
			use_deepseek=st.session_state.get("use_deepseek", False),
			use_local_llm=st.session_state.get("use_local_llm", False)
		)
	except FileNotFoundError as e:
		st.error(f"❌ {str(e)}\n\n💡 Tip: Make sure you entered a single, valid path without extra spaces.")
		st.stop()
	except Exception as e:
		st.error(f"❌ Error during analysis: {str(e)}")
		st.exception(e)
		st.stop()
	
	# Handle AI balance detection after streaming
	if st.session_state.get("use_deepseek", False) and st.session_state.get("deepseek_api_key"):
		try:
			if any("Insufficient Balance" in (iss.get("ai_justification", "") or "") for iss in issues):
				st.warning("🔑 DeepSeek: Insufficient balance. AI features have been temporarily disabled for this session. The rest of the analysis is available.")
				st.session_state.use_deepseek = False
				st.session_state.ai_insufficient_balance = True
		except Exception:
			pass
	
	st.session_state.root = root
	st.session_state.repo = repo  # Store full repo data
	st.session_state.repo_summary = repo.get("summary", {}) | {"languages": repo.get("languages", [])}
	
	# Create DataFrame with AI-enhanced columns if available
	df_columns = ["severity", "category", "source", "file", "start_line", "title", "description"]
	if issues and any("ai_severity" in issue for issue in issues if isinstance(issue, dict)):
		df_columns.extend(["ai_severity", "ai_justification", "ai_suggestions"])
	
	# Create DataFrame and only include columns that exist in the data
	if issues:
		df = pd.DataFrame(issues)
		available_columns = [col for col in df_columns if col in df.columns]
		st.session_state.issues_df = df[available_columns]
	else:
		st.session_state.issues_df = pd.DataFrame()
	st.session_state.hotspots_df = pd.DataFrame(hotspots, columns=["file", "hotspot_score"]) if hotspots else pd.DataFrame(columns=["file", "hotspot_score"])
	
	msg = "Fast analysis completed." if fast_mode else "Analysis completed."
	if st.session_state.get("use_deepseek", False):
		msg += " + DeepSeek Enhanced"
	elif st.session_state.get("use_local_llm", False):
		msg += " + Local LLM Enhanced"
	st.success(msg)

repo_summary = st.session_state.repo_summary
issues_df = st.session_state.issues_df
hotspots_df = st.session_state.hotspots_df
root = st.session_state.root

if repo_summary is not None and issues_df is not None:
	# Enhanced Overview KPIs with custom styling
	st.markdown("### 📊 Analysis Overview")
	
	# Add issue count to repo summary for components
	repo_summary["issue_count"] = len(issues_df)
	if 'create_metrics_cards' in globals() and callable(globals()['create_metrics_cards']):
		try:
			create_metrics_cards(repo_summary)
		except Exception as e:
			st.warning(f"Could not render metrics cards: {e}")
	else:
		# Fallback: show basic metrics
		col1, col2, col3, col4 = st.columns(4)
		with col1:
			st.metric("Total Issues", len(issues_df))
		with col2:
			st.metric("Files Analyzed", repo_summary.get("file_count", 0))
		with col3:
			st.metric("Lines of Code", repo_summary.get("sloc", 0))
		with col4:
			st.metric("Languages", len(repo_summary.get("languages", [])))

	tabs = st.tabs(["📊 Dashboards", "⚠️ Issues", "📁 File Details", "🔧 Autofix", "📤 Export", "🔗 Dependencies", "🔥 Hotspots", "📈 Trends", "🤖 AI Q&A"]) 

	with tabs[0]:
		# Enhanced Filters with better styling
		st.markdown("### 🔍 Smart Filters")
		f1, f2, f3 = st.columns(3)
		sev_opts = sorted(issues_df["severity"].unique()) if not issues_df.empty else []
		cat_opts = sorted(issues_df["category"].unique()) if not issues_df.empty else []
		src_opts = sorted(issues_df["source"].unique()) if not issues_df.empty else []
		sev_sel = f1.multiselect("🚨 Severity", options=sev_opts, default=sev_opts, key="sev_sel")
		cat_sel = f2.multiselect("📂 Category", options=cat_opts, default=cat_opts, key="cat_sel")
		src_sel = f3.multiselect("🔧 Source", options=src_opts, default=src_opts, key="src_sel")

		filtered = issues_df.copy()
		if not filtered.empty:
			filtered = filtered[
				filtered["severity"].isin(sev_sel)
				& filtered["category"].isin(cat_sel)
				& filtered["source"].isin(src_sel)
			]

		st.markdown("### 📈 Visual Analytics")
		
		# Quality Score Gauge
		st.markdown("#### 🎯 Code Quality Score")
		_safe_render("quality score gauge", create_quality_score_gauge, filtered)
		
		# Charts in columns
		c1, c2 = st.columns(2)
		with c1:
			st.markdown("#### 🚨 Severity Distribution")
			_safe_render("severity chart", create_severity_chart, filtered)
		with c2:
			st.markdown("#### 🔥 Code Hotspots")
			_safe_render("hotspots chart", create_hotspots_chart, hotspots_df)
		
		# Additional charts
		c3, c4 = st.columns(2)
		with c3:
			st.markdown("#### 📊 Language Distribution")
			_safe_render("language distribution chart", create_language_distribution_chart, repo_summary)
		with c4:
			st.markdown("#### 📈 Quality Trends")
			_safe_render("quality trends chart", create_trend_chart, filtered, st.session_state.repo)

	with tabs[1]:
		st.markdown("### ⚠️ Issue Management")
		q = st.text_input("🔍 Search in title/description/file", key="search_q", placeholder="Type to search issues...")
		show = issues_df
		if not show.empty and q:
			q_lower = q.lower()
			show = show[show.apply(lambda r: q_lower in str(r["title"]).lower() or q_lower in str(r["description"]).lower() or q_lower in str(r["file"]).lower(), axis=1)]
		
		# Enhanced rendering with colored badges
		def badge(sev: str) -> str:
			cls = {
				"critical": "badge badge-critical",
				"high": "badge badge-high",
				"medium": "badge badge-medium",
				"low": "badge badge-low",
			}.get(sev, "badge")
			return f"<span class='{cls}'>{sev}</span>"
		
		if not show.empty:
			st.markdown(f"**Found {len(show)} issues**")
			styled = show.copy()
			styled["severity"] = styled["severity"].apply(lambda x: badge(str(x)))
			html_table = styled.to_html(escape=False, index=False)
			st.markdown(f"<div class='table-container'>{html_table}</div>", unsafe_allow_html=True)
		else:
			st.info("🎉 No issues found! Your code looks clean.")

	with tabs[2]:
		st.markdown("### 📁 File Details & Code Context")
		if not issues_df.empty:
			# Group issues by file
			file_issues = issues_df.groupby('file').apply(lambda x: x.to_dict('records'), include_groups=False).to_dict()
			selected_file = st.selectbox("📂 Select file to view details:", list(file_issues.keys()))
			
			if selected_file:
				file_issues_list = file_issues[selected_file]
				st.markdown(
					f"""
					<div class="file-detail-card">
						<h4>📄 {selected_file}</h4>
						<p><strong>{len(file_issues_list)} issues found</strong></p>
					</div>
					""",
					unsafe_allow_html=True,
				)
				
				# Try to read and display file content
				if root is not None:
					file_path = root / selected_file
					if file_path.exists():
						try:
							content = file_path.read_text(encoding='utf-8')
							lines = content.splitlines()
							
							# Show issues for this file with enhanced styling
							for issue in file_issues_list:
								line_num = issue['start_line']
								severity = issue['severity']
								title = issue['title']
								source = issue['source']
								
								severity_emoji = {"critical": "🔴", "high": "🟠", "medium": "🟡", "low": "🟢"}.get(severity, "⚪")
								
								with st.expander(f"{severity_emoji} Line {line_num}: {title} ({source}) - {severity.upper()}"):
									st.markdown(f"**📝 Description:** {issue['description']}")
									if issue.get('suggested_fix'):
										st.markdown(f"**💡 Suggested Fix:** {issue['suggested_fix']}")
									
									# Show code context around the issue
									start_ctx = max(0, line_num - 3)
									end_ctx = min(len(lines), line_num + 2)
									
									st.markdown("**🔍 Code Context:**")
									context_lines = lines[start_ctx:end_ctx]
									
									# Create custom code snippet with syntax highlighting
									code_html = '<div class="code-snippet">'
									for i, line in enumerate(context_lines):
										actual_line = start_ctx + i + 1
										line_class = "highlight-line" if actual_line == line_num else ""
										arrow = "→" if actual_line == line_num else " "
										code_html += f'<div class="{line_class}"><span class="line-number">{arrow} {actual_line:3d}:</span>{line}</div>'
									code_html += '</div>'
									
									st.markdown(code_html, unsafe_allow_html=True)
						except Exception as e:
							st.error(f"❌ Could not read file: {e}")
					else:
						st.error("❌ File not found")
				else:
					st.error("❌ No repository loaded")
		else:
			st.info("🎉 No issues to display - your code is clean!")

	with tabs[3]:
		st.markdown("### 🔧 Smart Autofix")
		if root is None:
			st.error("❌ Run analysis first.")
		else:
			issues_for_fix: List[Issue] = []
			for _, r in issues_df.iterrows():
				issues_for_fix.append({
					"id": "",
					"title": r.get("title", ""),
					"description": r.get("description", ""),
					"category": r.get("category", "other"),
					"severity": r.get("severity", "low"),
					"confidence": "high",
					"file": r.get("file", ""),
					"start_line": int(r.get("start_line", 1)),
					"end_line": int(r.get("start_line", 1)),
					"evidence": "",
					"suggested_fix": "",
					"references": [],
					"source": r.get("source", ""),
					"tags": [],
				})
			edits = compute_autofixes(root, issues_for_fix)
			
			if edits:
				st.markdown(
					f"""
					<div style="background: linear-gradient(135deg, #27ae60, #2ecc71); color: white; padding: 1rem; border-radius: 10px; margin-bottom: 1rem;">
						<h4>🎯 Found {len(edits)} Safe Autofixes</h4>
						<p>These are unused import removals that can be safely applied.</p>
					</div>
					""",
					unsafe_allow_html=True,
				)
				
				patch_text = generate_patch(edits, root)
				st.markdown("**📋 Preview Changes:**")
				st.code(patch_text, language="diff")
				
				col1, col2 = st.columns(2)
				with col1:
					if st.button("🚀 Apply Autofixes", type="primary", use_container_width=True):
						if st.session_state.get("autofix_confirmed", False):
							results = apply_edits(edits)
							applied = sum(1 for _, ok in results if ok)
							st.success(f"✅ Applied {applied}/{len(results)} autofixes successfully!")
							st.session_state.autofix_confirmed = False
							# Clear cache to force re-analysis
							run_analysis_cached.clear()
						else:
							st.session_state.autofix_confirmed = True
							st.warning("⚠️ Click again to confirm applying autofixes to your files.")
				with col2:
					if st.session_state.get("autofix_confirmed", False):
						if st.button("❌ Cancel", use_container_width=True):
							st.session_state.autofix_confirmed = False
							st.rerun()
			else:
				st.info("🎉 No safe autofixes found - your code is already optimized!")

	with tabs[4]:
		st.markdown("### 📤 Export & Reports")
		if root is not None:
			st.markdown("**📊 Generate comprehensive reports for your team:**")
			
			col1, col2 = st.columns(2)
			
			with col1:
				md_text = build_markdown_text(root, repo_summary, issues_df.to_dict(orient="records") if not issues_df.empty else [], hotspots_df.values.tolist() if hotspots_df is not None else None)
				st.download_button(
					"📄 Download Markdown Report", 
					md_text, 
					file_name="cq-report.md",
					mime="text/markdown",
					use_container_width=True
				)
			
			with col2:
				csv_buf = io.StringIO()
				issues_df.to_csv(csv_buf, index=False)
				st.download_button(
					"📊 Download CSV (Issues)", 
					csv_buf.getvalue(), 
					file_name="cq-issues.csv", 
					mime="text/csv",
					use_container_width=True
				)
			
			st.markdown("---")
			st.markdown(
				"""
				<div style="background: rgba(102, 126, 234, 0.1); padding: 1rem; border-radius: 10px; border-left: 4px solid #667eea;">
					<h4>💡 Pro Tips:</h4>
					<ul>
						<li><strong>Markdown Report:</strong> Perfect for team reviews and documentation</li>
						<li><strong>CSV Export:</strong> Import into project management tools or spreadsheets</li>
						<li><strong>SARIF:</strong> Use CLI for IDE/CI integration: <code>cq-agent analyze . --sarif report.sarif</code></li>
					</ul>
				</div>
				""",
				unsafe_allow_html=True,
			)

	with tabs[5]:  # Dependencies tab
		st.markdown("### 🔗 Advanced Code Dependencies & Relationships")
		
		if root is not None and 'repo' in st.session_state:
			# Create advanced dependency visualizations
			with st.spinner("🔍 Analyzing code dependencies..."):
				dep_viz = create_advanced_dependency_visualizations(st.session_state.repo)
			
			# Display metrics cards
			if dep_viz.get('metrics_cards'):
				st.markdown("#### 📊 Dependency Metrics")
				metrics_cards = dep_viz['metrics_cards']
				
				# Create 3 rows of 2 cards each
				for i in range(0, len(metrics_cards), 2):
					cols = st.columns(2)
					for j, col in enumerate(cols):
						if i + j < len(metrics_cards):
							card = metrics_cards[i + j]
							with col:
								st.markdown(f"""
								<div style="background: linear-gradient(135deg, {card['color']}, {card['color']}80); 
											padding: 1rem; border-radius: 15px; margin: 0.5rem 0; 
											box-shadow: 0 8px 32px rgba(0,0,0,0.1);">
									<div style="display: flex; align-items: center; justify-content: space-between;">
										<div>
											<h3 style="color: white; margin: 0; font-size: 1.5rem;">{card['value']}</h3>
											<p style="color: rgba(255,255,255,0.9); margin: 0.5rem 0 0 0; font-size: 0.9rem;">{card['title']}</p>
										</div>
										<div style="font-size: 2rem;">{card['icon']}</div>
									</div>
								</div>
								""", unsafe_allow_html=True)
			
			# Visualization tabs
			viz_tabs = st.tabs(["🌐 Network Graph", "🌞 Hierarchy", "🔥 Heatmap", "📊 Centrality"])
			
			with viz_tabs[0]:  # Network Graph
				st.markdown("#### Interactive Dependency Network")
				if dep_viz.get('network_graph'):
					st.plotly_chart(dep_viz['network_graph'], use_container_width=True, key="dep_network")
					st.markdown("""
					<div style="background: rgba(255, 255, 255, 0.1); padding: 1rem; border-radius: 10px; margin: 1rem 0;">
						<h4>💡 How to Use This Graph:</h4>
						<ul>
							<li><strong>Hover</strong> over nodes to see detailed file information</li>
							<li><strong>Drag</strong> nodes to explore the network structure</li>
							<li><strong>Zoom</strong> in/out to focus on specific areas</li>
							<li><strong>Node size</strong> indicates centrality and connections</li>
							<li><strong>Node color</strong> represents programming language</li>
						</ul>
					</div>
					""", unsafe_allow_html=True)
			
			with viz_tabs[1]:  # Hierarchy
				st.markdown("#### Dependency Hierarchy")
				if dep_viz.get('sunburst'):
					st.plotly_chart(dep_viz['sunburst'], use_container_width=True, key="dep_sunburst")
					st.markdown("""
					<div style="background: rgba(255, 255, 255, 0.1); padding: 1rem; border-radius: 10px; margin: 1rem 0;">
						<h4>🌞 Sunburst Chart Features:</h4>
						<ul>
							<li><strong>Hierarchical view</strong> of your codebase structure</li>
							<li><strong>Size</strong> represents number of connections</li>
							<li><strong>Color</strong> indicates programming language</li>
							<li><strong>Click</strong> to drill down into specific directories</li>
						</ul>
					</div>
					""", unsafe_allow_html=True)
			
			with viz_tabs[2]:  # Heatmap
				st.markdown("#### Dependency Matrix")
				if dep_viz.get('heatmap'):
					st.plotly_chart(dep_viz['heatmap'], use_container_width=True, key="dep_heatmap")
					st.markdown("""
					<div style="background: rgba(255, 255, 255, 0.1); padding: 1rem; border-radius: 10px; margin: 1rem 0;">
						<h4>🔥 Heatmap Insights:</h4>
						<ul>
							<li><strong>Blue cells</strong> indicate dependencies between files</li>
							<li><strong>Rows</strong> show files that depend on others</li>
							<li><strong>Columns</strong> show files that are depended upon</li>
							<li><strong>Darker blue</strong> = stronger dependency relationship</li>
						</ul>
					</div>
					""", unsafe_allow_html=True)
			
			with viz_tabs[3]:  # Centrality
				st.markdown("#### Centrality Analysis")
				if dep_viz.get('centrality_analysis'):
					st.plotly_chart(dep_viz['centrality_analysis'], use_container_width=True, key="dep_centrality")
					st.markdown("""
					<div style="background: rgba(255, 255, 255, 0.1); padding: 1rem; border-radius: 10px; margin: 1rem 0;">
						<h4>📊 Centrality Metrics Explained:</h4>
						<ul>
							<li><strong>Degree Centrality:</strong> Number of direct connections</li>
							<li><strong>Closeness Centrality:</strong> How close a file is to all other files</li>
							<li><strong>Betweenness Centrality:</strong> How often a file lies on shortest paths</li>
							<li><strong>Language Distribution:</strong> Programming language breakdown</li>
						</ul>
					</div>
					""", unsafe_allow_html=True)
			
			# Advanced insights section
			metrics = dep_viz.get('metrics', {})
			if metrics:
				st.markdown("#### 🔍 Advanced Insights")
				
				# Circular dependencies warning
				if metrics.get('circular_dependencies'):
					st.warning(f"⚠️ **Circular Dependencies Detected!** Found {len(metrics['circular_dependencies'])} circular dependency chains that may cause issues.")
					with st.expander("View Circular Dependencies"):
						for i, cycle in enumerate(metrics['circular_dependencies'][:5], 1):
							st.code(f"Cycle {i}: {' → '.join(cycle)} → {cycle[0]}")
				
				# Orphaned files
				if metrics.get('orphaned_files'):
					st.info(f"🏝️ **Orphaned Files:** {len(metrics['orphaned_files'])} files have no dependencies. Consider if they should be connected to the main codebase.")
					with st.expander("View Orphaned Files"):
						for file in metrics['orphaned_files'][:10]:
							st.code(Path(file).name)
				
				# Language distribution
				lang_dist = metrics.get('language_distribution', {})
				if lang_dist:
					st.success(f"📈 **Language Distribution:** {', '.join([f'{lang}: {count} files' for lang, count in lang_dist.items()])}")
				
				# Complexity insights
				complexity_dist = metrics.get('complexity_distribution', {})
				if complexity_dist:
					high_complexity = complexity_dist.get('high', 0)
					if high_complexity > 0:
						st.warning(f"⚠️ **High Complexity Files:** {high_complexity} files have high complexity. Consider refactoring.")
					else:
						st.success("✅ **Complexity:** All files have manageable complexity levels.")
		else:
			st.info("Upload a repository to see dependency analysis")

	with tabs[6]:  # Hotspots tab
		st.markdown("### 🔥 Code Hotspots Analysis")
		if root is not None and hotspots_df is not None and 'repo' in st.session_state:
			# Create hotspot visualizations
			hotspots_list = hotspots_df.values.tolist() if not hotspots_df.empty else []
			hotspot_viz = create_hotspot_visualizations(st.session_state.repo, hotspots_list)
			
			# Show metrics
			if hotspot_viz.get('metrics'):
				metrics = hotspot_viz['metrics']
				col1, col2, col3, col4 = st.columns(4)
				with col1:
					st.metric("High Hotspot Files", metrics.get('high_hotspot_files', 0))
				with col2:
					st.metric("Avg Hotspot Score", f"{metrics.get('average_hotspot_score', 0):.3f}")
				with col3:
					st.metric("Most Complex File", Path(metrics.get('most_complex_file', 'N/A')).name if metrics.get('most_complex_file') else 'N/A')
				with col4:
					st.metric("Most Churned File", Path(metrics.get('most_churned_file', 'N/A')).name if metrics.get('most_churned_file') else 'N/A')
			
			# Show visualizations
			tab1, tab2, tab3, tab4 = st.tabs(["Heatmap", "Scatter Plot", "Language Comparison", "Treemap"])
			
			with tab1:
				if hotspot_viz.get('heatmap'):
					st.plotly_chart(hotspot_viz['heatmap'], use_container_width=True, key="hot_heatmap")
			
			with tab2:
				if hotspot_viz.get('scatter'):
					st.plotly_chart(hotspot_viz['scatter'], use_container_width=True, key="hot_scatter")
			
			with tab3:
				if hotspot_viz.get('language_comparison'):
					st.plotly_chart(hotspot_viz['language_comparison'], use_container_width=True, key="hot_lang_comp")
			
			with tab4:
				if hotspot_viz.get('treemap'):
					st.plotly_chart(hotspot_viz['treemap'], use_container_width=True, key="hot_treemap")
		else:
			st.info("Upload a repository to see hotspot analysis")

	with tabs[7]:  # Trends tab
		st.markdown("### 📈 Quality Trends Over Time")
		if root is not None:
			# Create trend visualizations
			trend_viz = create_trend_visualizations(str(root), days_back=30)
			
			# Show metrics
			if trend_viz.get('metrics'):
				metrics = trend_viz['metrics']
				col1, col2, col3, col4 = st.columns(4)
				with col1:
					st.metric("Total Commits", metrics.get('total_commits', 0))
				with col2:
					st.metric("Avg Files/Commit", f"{metrics.get('avg_files_per_commit', 0):.1f}")
				with col3:
					st.metric("Quality Trend", f"{'📈' if metrics.get('quality_trend', 0) > 0 else '📉'} {metrics.get('quality_trend', 0):.3f}")
				with col4:
					st.metric("Net Lines Change", metrics.get('net_lines_change', 0))
			
			# LangGraph Intelligent Analysis
			if 'repo' in st.session_state and trend_viz.get('trend_data'):
				st.markdown("### 🧠 AI-Powered Trend Analysis")
				with st.spinner("Analyzing trends with LangGraph..."):
					langgraph_analysis = create_langgraph_trend_analysis(
						st.session_state.repo, 
						trend_viz['trend_data']
					)
				
				# Display insights
				if langgraph_analysis.get('insights'):
					st.markdown("#### 📊 Key Insights")
					for insight in langgraph_analysis['insights']:
						if hasattr(insight, 'type'):
							# TrendInsight object
							confidence_color = "🟢" if insight.confidence > 0.7 else "🟡" if insight.confidence > 0.4 else "🔴"
							st.markdown(f"""
							<div style=\"background: rgba(255, 255, 255, 0.1); padding: 1rem; border-radius: 10px; margin: 0.5rem 0;\">
								<h4>{confidence_color} {insight.description}</h4>
								<p><strong>Recommendation:</strong> {insight.recommendation}</p>
								<p><strong>Confidence:</strong> {insight.confidence:.2f}</p>
							</div>
							""", unsafe_allow_html=True)
						else:
							# Dict insight
							confidence_color = "🟢" if insight.get('confidence', 0) > 0.7 else "🟡" if insight.get('confidence', 0) > 0.4 else "🔴"
							st.markdown(f"""
							<div style=\"background: rgba(255, 255, 255, 0.1); padding: 1rem; border-radius: 10px; margin: 0.5rem 0;\">
								<h4>{confidence_color} {insight.get('description', 'No description')}</h4>
								<p><strong>Confidence:</strong> {insight.get('confidence', 0):.2f}</p>
							</div>
							""", unsafe_allow_html=True)
				
				# Display recommendations
				if langgraph_analysis.get('recommendations'):
					st.markdown("#### 💡 Actionable Recommendations")
					for rec in langgraph_analysis['recommendations']:
						priority_color = {"high": "🔴", "medium": "🟡", "low": "🟢"}.get(rec.get('priority', 'medium'), '🟡')
						st.markdown(f"""
						<div style=\"background: rgba(255, 255, 255, 0.1); padding: 1rem; border-radius: 10px; margin: 0.5rem 0;\">
							<h4>{priority_color} {rec.get('title', 'Recommendation')}</h4>
							<p><strong>Description:</strong> {rec.get('description', 'No description')}</p>
							<p><strong>Actions:</strong></p>
							<ul>
								{''.join([f'<li>{action}</li>' for action in rec.get('actions', [])])}
							</ul>
						</div>
						""", unsafe_allow_html=True)
				
				# Overall confidence
				confidence = langgraph_analysis.get('confidence', 0)
				st.markdown(f"""
				<div style=\"background: linear-gradient(135deg, #667eea, #764ba2); padding: 1rem; border-radius: 10px; margin: 1rem 0;\">
					<h3>🎯 Analysis Confidence: {confidence:.1%}</h3>
					<p>Based on data quality and trend consistency</p>
				</div>
				""", unsafe_allow_html=True)
			
			# Show visualizations
			tab1, tab2, tab3, tab4 = st.tabs(["Quality Trends", "Commit Activity", "Lines Changed", "Developer Activity"])
			
			with tab1:
				if trend_viz.get('quality_trend'):
					st.plotly_chart(trend_viz['quality_trend'], use_container_width=True, key="trend_quality")
			
			with tab2:
				if trend_viz.get('commit_activity'):
					st.plotly_chart(trend_viz['commit_activity'], use_container_width=True, key="trend_commits")
			
			with tab3:
				if trend_viz.get('lines_changed'):
					st.plotly_chart(trend_viz['lines_changed'], use_container_width=True, key="trend_lines")
			
			with tab4:
				if trend_viz.get('developer_activity'):
					st.plotly_chart(trend_viz['developer_activity'], use_container_width=True, key="trend_devs")
		else:
			st.info("Upload a repository to see trend analysis")

	with tabs[8]:  # AI Q&A tab
		st.markdown("### 🤖 AI-Powered Code Q&A")
		
		use_ai = bool(st.session_state.get("use_deepseek", False) or st.session_state.get("use_local_llm", False))
		insufficient = bool(st.session_state.get("ai_insufficient_balance"))
		
		if insufficient:
			st.warning("🔑 DeepSeek: Insufficient balance. Switching to Local LLM fallback...")
			st.session_state.use_deepseek = False
			st.session_state.use_local_llm = True
			use_ai = True
		elif not use_ai:
			st.info("ℹ️ AI features are disabled. Enable AI in the sidebar to use Q&A.")
			st.markdown("""
			**Available AI options:**
			- **DeepSeek (Remote)**: Requires API key, most capable
			- **Local LLM (Fast)**: No API key, offline, good for development
			
			Enable one in the sidebar to start asking questions about your code.
			""")
		elif root is not None and 'repo' in st.session_state:
			# AI Q&A Interface
			st.markdown("#### 💬 Ask questions about your codebase")
			
			# Example questions
			with st.expander("💡 Example Questions"):
				st.markdown("""
				- "What are the main security vulnerabilities in this codebase?"
				- "How can I improve the performance of the authentication module?"
				- "What design patterns are used in this project?"
				- "Where are the most complex functions and how can I simplify them?"
				- "What are the dependencies between different modules?"
				- "How can I refactor the database access layer?"
				""")
			
			# Question input
			question = st.text_area(
				"Ask a question about your codebase:",
				placeholder="e.g., What are the main security issues in this codebase?",
				height=100
			)
			
			col1, col2 = st.columns([1, 4])
			with col1:
				ask_button = st.button("🚀 Ask AI", type="primary", use_container_width=True)
			
			# Process question
			if ask_button and question.strip():
				with st.spinner("🤖 AI is analyzing your codebase..."):
					try:
						if st.session_state.get("use_deepseek", False):
							# DeepSeek path
							if 'answer_codebase_question' in globals() and callable(globals()['answer_codebase_question']):
								try:
									answer = answer_codebase_question(
										question.strip(), 
										st.session_state.repo, 
										st.session_state.deepseek_api_key
									)
								except Exception as e:
									answer = f"Error: {str(e)}"
							else:
								answer = "AI backend not available"
							# Handle insufficient balance gracefully
							if "Insufficient Balance" in (answer or ""):
								st.warning("🔑 DeepSeek: Insufficient balance. Switching to Local LLM fallback...")
								st.session_state.use_deepseek = False
								st.session_state.use_local_llm = True
								# Retry with local LLM
								if run_agentic_qa is not None:
									answer, _ = run_agentic_qa(question.strip(), st.session_state.repo, backend="local", model="microsoft/DialoGPT-small")
							ai_backend_name = "DeepSeek"
						elif st.session_state.get("use_local_llm", False) and run_agentic_qa is not None:
							# Local LLM path
							answer, _ = run_agentic_qa(question.strip(), st.session_state.repo, backend="local", model="microsoft/DialoGPT-small")
							ai_backend_name = "Local LLM"
						else:
							answer = "AI backend not available"
							ai_backend_name = "None"
						
						if answer and not answer.startswith("AI backend not available"):
							st.markdown(f"#### 🤖 {ai_backend_name} Response")
							st.markdown(f"""
							<div style=\"background: rgba(102, 126, 234, 0.1); padding: 1.5rem; border-radius: 15px; 
									border-left: 4px solid #667eea; margin: 1rem 0;\">
								{answer}
							</div>
							""", unsafe_allow_html=True)
						
					except Exception as e:
						st.error(f"❌ Error getting AI response: {e}")
			
			# AI-Enhanced Issues Section
			if not issues_df.empty and any("ai_severity" in col for col in issues_df.columns):
				st.markdown("---")
				st.markdown("#### 🧠 AI-Enhanced Issue Analysis")
				
				# Show AI severity vs original severity comparison
				if "ai_severity" in issues_df.columns:
					ai_severity_counts = issues_df["ai_severity"].value_counts()
					original_severity_counts = issues_df["severity"].value_counts()
					
					col1, col2 = st.columns(2)
					with col1:
						st.markdown("**Original Severity**")
						for severity, count in original_severity_counts.items():
							st.write(f"• {severity.title()}: {count}")
					
					with col2:
						st.markdown("**AI-Enhanced Severity**")
						for severity, count in ai_severity_counts.items():
							st.write(f"• {severity.title()}: {count}")
				
				# Show AI suggestions for top issues
				if "ai_suggestions" in issues_df.columns:
					st.markdown("#### 💡 AI Suggestions for Top Issues")
					top_issues = issues_df.head(3)
					
					for idx, issue in top_issues.iterrows():
						with st.expander(f"🔍 {issue['title']} ({issue.get('ai_severity', issue['severity']).title()})"):
							st.markdown(f"**File:** `{issue['file']}`")
							st.markdown(f"**Description:** {issue['description']}")
							
							if "ai_justification" in issue and pd.notna(issue["ai_justification"]):
								st.markdown(f"**AI Analysis:** {issue['ai_justification']}")
							
							if "ai_suggestions" in issue and pd.notna(issue["ai_suggestions"]):
								st.markdown(f"**AI Suggestions:** {issue['ai_suggestions']}")
		else:
			st.info("Run analysis first to enable AI Q&A features")

else:
	st.markdown(
		"""
		<div style="text-align: center; padding: 3rem; background: rgba(255, 255, 255, 0.1); border-radius: 15px; margin: 2rem 0;">
			<h3 style="color: #2c3e50; font-family: 'Inter', sans-serif;">🚀 Ready to Analyze Your Code?</h3>
			<p style="color: #7f8c8d; font-size: 1.1rem; margin: 1rem 0;">Set a repository path in the sidebar and click <strong>"Run Analysis"</strong> to get started!</p>
			<div style="margin-top: 2rem;">
				<span style="background: linear-gradient(135deg, #667eea, #764ba2); color: white; padding: 0.5rem 1rem; border-radius: 20px; font-weight: 600;">✨ AI-Powered Code Quality Analysis</span>
			</div>
		</div>
		""",
		unsafe_allow_html=True,
	)
