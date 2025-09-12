"""
Advanced Visualizations Package
Provides interactive charts and visualizations for code quality analysis
"""

from .dependency_graph import create_dependency_visualization
from .hotspots import create_hotspot_visualizations
from .trends import create_trend_visualizations

__all__ = [
    'create_dependency_visualization',
    'create_hotspot_visualizations', 
    'create_trend_visualizations'
]
