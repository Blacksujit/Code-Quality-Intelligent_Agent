"""
Advanced Dependency Visualization Module
Creates interactive dependency graphs and code relationship maps
"""

import networkx as nx
import plotly.graph_objects as go
from typing import Dict, List, Tuple, Set
import pandas as pd
from pathlib import Path
import ast
import re


class DependencyVisualizer:
    """Creates interactive dependency visualizations"""
    
    def __init__(self):
        self.graph = nx.DiGraph()
        self.file_dependencies = {}
        self.function_dependencies = {}
        
    def build_dependency_graph(self, repo_data: Dict) -> nx.DiGraph:
        """Build comprehensive dependency graph from repository data"""
        self.graph.clear()
        
        # Handle both RepoContext and dict formats
        if hasattr(repo_data, 'files'):
            files_dict = repo_data.files
        else:
            files_dict = repo_data.get('files', {})
        
        # Add files as nodes
        for file_path, file_data in files_dict.items():
            # Handle both FileRecord and dict formats
            if hasattr(file_data, 'language'):
                language = file_data.language
                sloc = file_data.sloc
                content = file_data.text
            else:
                language = file_data.get('language', 'unknown')
                sloc = file_data.get('sloc', 0)
                content = file_data.get('text', '')
            
            self.graph.add_node(
                file_path,
                type='file',
                language=language,
                sloc=sloc,
                complexity=0,  # Will be calculated later
                issues_count=0  # Will be calculated later
            )
        
        # Build dependencies
        self._build_file_dependencies(repo_data)
        self._build_function_dependencies(repo_data)
        
        return self.graph
    
    def _build_file_dependencies(self, repo_data: Dict):
        """Build file-level dependencies"""
        # Handle both RepoContext and dict formats
        if hasattr(repo_data, 'files'):
            files_dict = repo_data.files
        else:
            files_dict = repo_data.get('files', {})
            
        for file_path, file_data in files_dict.items():
            # Handle both FileRecord and dict formats
            if hasattr(file_data, 'language'):
                language = file_data.language
                content = file_data.text
            else:
                language = file_data.get('language', 'unknown')
                content = file_data.get('text', '')
                
            if language == 'python':
                self._parse_python_imports(file_path, content)
            elif language in ['javascript', 'typescript']:
                self._parse_js_imports(file_path, content)
    
    def _parse_python_imports(self, file_path: str, content: str):
        """Parse Python imports and create dependencies"""
        try:
            tree = ast.parse(content)
            
            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    for alias in node.names:
                        self._add_dependency(file_path, alias.name, 'import')
                elif isinstance(node, ast.ImportFrom):
                    if node.module:
                        self._add_dependency(file_path, node.module, 'from_import')
        except:
            pass  # Skip files that can't be parsed
    
    def _parse_js_imports(self, file_path: str, content: str):
        """Parse JavaScript/TypeScript imports"""
        
        # Match various import patterns
        import_patterns = [
            r"import\s+.*?\s+from\s+['\"]([^'\"]+)['\"]",  # import ... from '...'
            r"import\s+['\"]([^'\"]+)['\"]",  # import '...'
            r"require\(['\"]([^'\"]+)['\"]\)",  # require('...')
        ]
        
        for pattern in import_patterns:
            matches = re.findall(pattern, content)
            for match in matches:
                if not match.startswith('.'):  # Skip relative imports for now
                    self._add_dependency(file_path, match, 'import')
    
    def _add_dependency(self, source_file: str, target_module: str, dep_type: str):
        """Add dependency edge to graph"""
        if source_file != target_module:  # Avoid self-loops
            self.graph.add_edge(
                source_file, 
                target_module, 
                type=dep_type,
                weight=1
            )
    
    def _build_function_dependencies(self, repo_data: Dict):
        """Build function-level dependencies within files"""
        for file_path, file_data in repo_data.get('files', {}).items():
            if file_data.get('language') == 'python':
                self._parse_python_functions(file_path, file_data)
    
    def _parse_python_functions(self, file_path: str, file_data: Dict):
        """Parse Python function calls within files"""
        try:
            content = file_data.get('content', '')
            tree = ast.parse(content)
            
            functions = {}
            calls = []
            
            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef):
                    functions[node.name] = node
                elif isinstance(node, ast.Call):
                    if isinstance(node.func, ast.Name):
                        calls.append(node.func.id)
            
            # Add function call dependencies
            for call in calls:
                if call in functions:
                    # This is a local function call
                    pass  # Could add internal function dependencies here
        except:
            pass
    
    def create_interactive_dependency_graph(self) -> go.Figure:
        """Create interactive Plotly dependency graph"""
        if not self.graph.nodes():
            return go.Figure()
        
        # Calculate layout
        pos = nx.spring_layout(self.graph, k=3, iterations=50)
        
        # Prepare data for plotting
        edge_x = []
        edge_y = []
        edge_info = []
        
        for edge in self.graph.edges():
            x0, y0 = pos[edge[0]]
            x1, y1 = pos[edge[1]]
            edge_x.extend([x0, x1, None])
            edge_y.extend([y0, y1, None])
            edge_info.append(f"{edge[0]} → {edge[1]}")
        
        # Create edge trace
        edge_trace = go.Scatter(
            x=edge_x, y=edge_y,
            line=dict(width=2, color='#888'),
            hoverinfo='none',
            mode='lines',
            name='Dependencies'
        )
        
        # Prepare node data
        node_x = []
        node_y = []
        node_text = []
        node_info = []
        node_colors = []
        node_sizes = []
        
        for node in self.graph.nodes():
            x, y = pos[node]
            node_x.append(x)
            node_y.append(y)
            
            node_data = self.graph.nodes[node]
            node_text.append(Path(node).name)
            node_info.append(f"""
            <b>{Path(node).name}</b><br>
            Language: {node_data.get('language', 'unknown')}<br>
            SLOC: {node_data.get('sloc', 0)}<br>
            Issues: {node_data.get('issues_count', 0)}<br>
            Complexity: {node_data.get('complexity', 0)}
            """)
            
            # Color by language
            lang_colors = {
                'python': '#3776ab',
                'javascript': '#f7df1e',
                'typescript': '#3178c6',
                'unknown': '#6c757d'
            }
            node_colors.append(lang_colors.get(node_data.get('language', 'unknown'), '#6c757d'))
            
            # Size by SLOC
            sloc = node_data.get('sloc', 0)
            node_sizes.append(max(10, min(50, sloc / 10)))
        
        # Create node trace
        node_trace = go.Scatter(
            x=node_x, y=node_y,
            mode='markers+text',
            hoverinfo='text',
            text=node_text,
            textposition="middle center",
            hovertext=node_info,
            marker=dict(
                size=node_sizes,
                color=node_colors,
                line=dict(width=2, color='white'),
                opacity=0.8
            ),
            name='Files'
        )
        
        # Create figure
        fig = go.Figure(data=[edge_trace, node_trace],
                       layout=go.Layout(
                           title='Code Dependency Graph',
                           titlefont_size=16,
                           showlegend=True,
                           hovermode='closest',
                           margin=dict(b=20,l=5,r=5,t=40),
                           annotations=[ dict(
                               text="Interactive dependency visualization - hover for details",
                               showarrow=False,
                               xref="paper", yref="paper",
                               x=0.005, y=-0.002,
                               xanchor='left', yanchor='bottom',
                               font=dict(color='#666', size=12)
                           )],
                           xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                           yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                           plot_bgcolor='rgba(0,0,0,0)',
                           paper_bgcolor='rgba(0,0,0,0)'
                       ))
        
        return fig
    
    def create_dependency_metrics(self) -> Dict:
        """Calculate dependency metrics"""
        if not self.graph.nodes():
            return {}
        
        metrics = {
            'total_files': len(self.graph.nodes()),
            'total_dependencies': len(self.graph.edges()),
            'average_dependencies_per_file': len(self.graph.edges()) / len(self.graph.nodes()) if self.graph.nodes() else 0,
            'most_connected_file': None,
            'circular_dependencies': [],
            'orphaned_files': []
        }
        
        # Find most connected file
        if self.graph.nodes():
            in_degrees = dict(self.graph.in_degree())
            out_degrees = dict(self.graph.out_degree())
            total_degrees = {node: in_degrees.get(node, 0) + out_degrees.get(node, 0) 
                           for node in self.graph.nodes()}
            
            if total_degrees:
                metrics['most_connected_file'] = max(total_degrees, key=total_degrees.get)
        
        # Find circular dependencies
        try:
            cycles = list(nx.simple_cycles(self.graph))
            metrics['circular_dependencies'] = cycles[:5]  # Limit to first 5
        except:
            pass
        
        # Find orphaned files (no dependencies)
        orphaned = [node for node in self.graph.nodes() 
                   if self.graph.degree(node) == 0]
        metrics['orphaned_files'] = orphaned[:10]  # Limit to first 10
        
        return metrics


def create_dependency_visualization(repo_data: Dict) -> Tuple[go.Figure, Dict]:
    """Main function to create dependency visualization"""
    try:
        visualizer = DependencyVisualizer()
        graph = visualizer.build_dependency_graph(repo_data)
        fig = visualizer.create_interactive_dependency_graph()
        metrics = visualizer.create_dependency_metrics()
        
        return fig, metrics
    except Exception as e:
        print(f"Error creating dependency visualization: {e}")
        # Return empty figure and metrics
        return go.Figure(), {}
