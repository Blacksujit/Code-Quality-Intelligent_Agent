# Graph module for dependency analysis
from .deps import build_dependency_graph, compute_hotspots

__all__ = ["build_dependency_graph", "compute_hotspots"]
