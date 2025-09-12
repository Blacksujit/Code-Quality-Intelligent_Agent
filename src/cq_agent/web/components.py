"""
Production-grade UI components for the Code Quality Intelligence Agent
"""

import streamlit as st
import pandas as pd
from typing import Dict, List, Any, Tuple
import plotly.express as px
import plotly.graph_objects as go

def create_metrics_cards(metrics: Dict[str, Any]) -> None:
    """Create beautiful metric cards with animations"""
    cols = st.columns(4)
    
    cards_data = [
        ("📁", "Files", metrics.get("file_count", 0), "#667eea"),
        ("📝", "SLOC", metrics.get("sloc_total", 0), "#764ba2"),
        ("🌐", "Languages", len(metrics.get("languages", [])), "#f093fb"),
        ("⚠️", "Issues", metrics.get("issue_count", 0), "#f5576c")
    ]
    
    for i, (icon, label, value, color) in enumerate(cards_data):
        with cols[i]:
            st.markdown(
                f"""
                <div class="metric-card fade-in-up" style="border-left-color: {color};">
                    <div class="metric-value" style="color: {color};">{value:,}</div>
                    <div class="metric-label">{icon} {label}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )


def create_severity_chart(issues_df: pd.DataFrame) -> None:
    """Create an interactive severity distribution chart"""
    if issues_df is None or issues_df.empty:
        st.info("No issues to display")
        return
    
    try:
        severity_counts = issues_df['severity'].value_counts()
        
        # Create pie chart
        fig = px.pie(
            values=severity_counts.values,
            names=severity_counts.index,
            title="Issue Severity Distribution",
            color_discrete_map={
                'critical': '#e74c3c',
                'high': '#f39c12', 
                'medium': '#f1c40f',
                'low': '#27ae60'
            }
        )
        
        fig.update_traces(
            textposition='inside',
            textinfo='percent+label',
            hovertemplate='<b>%{label}</b><br>Count: %{value}<br>Percentage: %{percent}<extra></extra>'
        )
        
        fig.update_layout(
            showlegend=True,
            height=400,
            font=dict(family="Inter, sans-serif"),
            title_font_size=16
        )
        
        st.plotly_chart(fig, use_container_width=True)
    except Exception as e:
        st.error(f"Error creating severity chart: {e}")
        st.info("No issues to display")


def create_hotspots_chart(hotspots_df: pd.DataFrame) -> None:
    """Create an interactive hotspots bar chart"""
    if hotspots_df is None or hotspots_df.empty:
        st.info("No hotspots computed")
        return
    
    try:
        # Take top 10 hotspots
        top_hotspots = hotspots_df.head(10)
        
        fig = px.bar(
            top_hotspots,
            x='hotspot_score',
            y='file',
            orientation='h',
            title="Top 10 Code Hotspots",
            color='hotspot_score',
            color_continuous_scale='Reds'
        )
        
        fig.update_layout(
            height=400,
            font=dict(family="Inter, sans-serif"),
            title_font_size=16,
            yaxis={'categoryorder': 'total ascending'}
        )
        
        fig.update_traces(
            hovertemplate='<b>%{y}</b><br>Hotspot Score: %{x}<extra></extra>'
        )
        
        st.plotly_chart(fig, use_container_width=True)
    except Exception as e:
        st.error(f"Error creating hotspots chart: {e}")
        st.info("No hotspots computed")


def create_trend_chart(issues_df: pd.DataFrame) -> None:
    """Create a trend chart showing issues over time (mock data for demo)"""
    if issues_df.empty:
        st.info("No issues to display")
        return
    
    # Mock trend data for demonstration
    import numpy as np
    dates = pd.date_range(start='2024-01-01', periods=30, freq='D')
    trend_data = pd.DataFrame({
        'date': dates,
        'issues': np.random.poisson(5, 30).cumsum(),
        'resolved': np.random.poisson(3, 30).cumsum()
    })
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=trend_data['date'],
        y=trend_data['issues'],
        mode='lines+markers',
        name='Issues Found',
        line=dict(color='#e74c3c', width=3),
        marker=dict(size=6)
    ))
    
    fig.add_trace(go.Scatter(
        x=trend_data['date'],
        y=trend_data['resolved'],
        mode='lines+markers',
        name='Issues Resolved',
        line=dict(color='#27ae60', width=3),
        marker=dict(size=6)
    ))
    
    fig.update_layout(
        title="Code Quality Trends (Last 30 Days)",
        xaxis_title="Date",
        yaxis_title="Number of Issues",
        height=400,
        font=dict(family="Inter, sans-serif"),
        title_font_size=16,
        hovermode='x unified'
    )
    
    st.plotly_chart(fig, use_container_width=True)


def create_language_distribution_chart(repo_summary: Dict[str, Any]) -> None:
    """Create a language distribution chart"""
    languages = repo_summary.get("languages", {})
    if not languages:
        st.info("No language data available")
        return

    try:
        # Normalize languages into list of (Language, Files)
        data: List[Tuple[str, int]]
        if isinstance(languages, dict):
            data = list(languages.items())
        elif isinstance(languages, list):
            if len(languages) > 0 and isinstance(languages[0], (list, tuple)) and len(languages[0]) == 2:
                # Already list of (lang, count)
                data = [(str(lang), int(count)) for lang, count in languages]
            else:
                # Assume list of language names; count occurrences
                from collections import Counter
                counts = Counter([str(x) for x in languages])
                data = list(counts.items())
        else:
            st.info("No language data available")
            return

        if not data:
            st.info("No language data available")
            return

        lang_data = pd.DataFrame(data, columns=['Language', 'Files'])

        fig = px.bar(
            lang_data,
            x='Language',
            y='Files',
            title="Files by Programming Language",
            color='Files',
            color_continuous_scale='Blues'
        )

        fig.update_layout(
            height=300,
            font=dict(family="Inter, sans-serif"),
            title_font_size=16
        )

        st.plotly_chart(fig, use_container_width=True)
    except Exception as e:
        st.error(f"Error creating language distribution chart: {e}")
        st.info("No language data available")


def create_issue_timeline(issues_df: pd.DataFrame) -> None:
    """Create an issue timeline visualization"""
    if issues_df.empty:
        st.info("No issues to display")
        return
    
    # Mock timeline data for demonstration
    import numpy as np
    from datetime import datetime, timedelta
    
    # Create mock timeline data
    timeline_data = []
    for _, issue in issues_df.iterrows():
        timeline_data.append({
            'file': issue['file'],
            'line': issue['start_line'],
            'severity': issue['severity'],
            'title': issue['title'],
            'timestamp': datetime.now() - timedelta(days=np.random.randint(0, 30))
        })
    
    timeline_df = pd.DataFrame(timeline_data)
    
    # Create scatter plot
    severity_colors = {
        'critical': '#e74c3c',
        'high': '#f39c12',
        'medium': '#f1c40f', 
        'low': '#27ae60'
    }
    
    fig = px.scatter(
        timeline_df,
        x='timestamp',
        y='file',
        color='severity',
        size='line',
        hover_data=['title'],
        title="Issue Timeline by File",
        color_discrete_map=severity_colors
    )
    
    fig.update_layout(
        height=500,
        font=dict(family="Inter, sans-serif"),
        title_font_size=16
    )
    
    st.plotly_chart(fig, use_container_width=True)


def create_quality_score_gauge(issues_df: pd.DataFrame) -> None:
    """Create a quality score gauge"""
    if issues_df.empty:
        score = 100
    else:
        # Calculate quality score based on issues
        total_issues = len(issues_df)
        critical_issues = len(issues_df[issues_df['severity'] == 'critical'])
        high_issues = len(issues_df[issues_df['severity'] == 'high'])
        
        # Simple scoring algorithm
        score = max(0, 100 - (critical_issues * 20) - (high_issues * 10) - (total_issues * 2))
    
    fig = go.Figure(go.Indicator(
        mode = "gauge+number+delta",
        value = score,
        domain = {'x': [0, 1], 'y': [0, 1]},
        title = {'text': "Code Quality Score"},
        delta = {'reference': 80},
        gauge = {
            'axis': {'range': [None, 100]},
            'bar': {'color': "darkblue"},
            'steps': [
                {'range': [0, 50], 'color': "lightgray"},
                {'range': [50, 80], 'color': "yellow"},
                {'range': [80, 100], 'color': "green"}
            ],
            'threshold': {
                'line': {'color': "red", 'width': 4},
                'thickness': 0.75,
                'value': 90
            }
        }
    ))
    
    fig.update_layout(
        height=300,
        font=dict(family="Inter, sans-serif")
    )
    
    st.plotly_chart(fig, use_container_width=True)
