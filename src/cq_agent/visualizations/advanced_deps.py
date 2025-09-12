"""
Advanced Dependency Visualizations
Modern, interactive dependency graphs with multiple visualization strategies
"""

import networkx as nx
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
from typing import Dict, List, Tuple, Set, Optional
import ast
import re
from pathlib import Path
from collections import defaultdict, Counter
import math


class AdvancedDependencyVisualizer:
    """Advanced dependency visualization with multiple modern strategies"""
    
    def __init__(self):
        self.graph = nx.DiGraph()
        self.file_metrics = {}
        self.dependency_metrics = {}
        
    def build_advanced_dependency_graph(self, repo_data: Dict) -> Dict:
        """Build comprehensive dependency analysis"""
        self.graph.clear()
        self.file_metrics = {}
        
        # Handle both RepoContext and dict formats
        if hasattr(repo_data, 'files'):
            files_dict = repo_data.files
        else:
            files_dict = repo_data.get('files', {})
        
        # Build file nodes with enhanced metrics
        for file_path, file_data in files_dict.items():
            if hasattr(file_data, 'language'):
                language = file_data.language
                sloc = file_data.sloc
                content = file_data.text
            else:
                language = file_data.get('language', 'unknown')
                sloc = file_data.get('sloc', 0)
                content = file_data.get('text', '')
            
            # Calculate file metrics
            complexity = self._calculate_file_complexity(content, language)
            imports_count = self._count_imports(content, language)
            
            self.graph.add_node(
                file_path,
                type='file',
                language=language,
                sloc=sloc,
                complexity=complexity,
                imports_count=imports_count,
                centrality=0,  # Will be calculated later
                degree=0,  # Will be calculated later
                betweenness=0  # Will be calculated later
            )
            
            self.file_metrics[file_path] = {
                'language': language,
                'sloc': sloc,
                'complexity': complexity,
                'imports_count': imports_count
            }
        
        # Build dependencies
        self._build_file_dependencies(files_dict)
        
        # Calculate centrality metrics
        self._calculate_centrality_metrics()
        
        # Generate comprehensive metrics
        self.dependency_metrics = self._generate_dependency_metrics()
        
        return {
            'graph': self.graph,
            'file_metrics': self.file_metrics,
            'dependency_metrics': self.dependency_metrics
        }
    
    def _calculate_file_complexity(self, content: str, language: str) -> int:
        """Calculate file complexity based on language"""
        if language == 'python':
            try:
                tree = ast.parse(content)
                complexity = 1
                for node in ast.walk(tree):
                    if isinstance(node, (ast.If, ast.While, ast.For, ast.AsyncFor)):
                        complexity += 1
                    elif isinstance(node, ast.ExceptHandler):
                        complexity += 1
                    elif isinstance(node, (ast.And, ast.Or)):
                        complexity += 1
                return complexity
            except:
                return 1
        else:
            # Simple complexity for JS/TS
            return content.count('if') + content.count('for') + content.count('while') + 1
    
    def _count_imports(self, content: str, language: str) -> int:
        """Count imports in file"""
        if language == 'python':
            try:
                tree = ast.parse(content)
                imports = 0
                for node in ast.walk(tree):
                    if isinstance(node, (ast.Import, ast.ImportFrom)):
                        imports += 1
                return imports
            except:
                return 0
        else:
            # Count JS/TS imports
            import_patterns = [
                r"import\s+.*?from\s+['\"][^'\"]+['\"]",
                r"import\s+['\"][^'\"]+['\"]",
                r"require\s*\(['\"][^'\"]+['\"]\)"
            ]
            imports = 0
            for pattern in import_patterns:
                imports += len(re.findall(pattern, content))
            return imports
    
    def _build_file_dependencies(self, files_dict: Dict):
        """Build file-level dependencies"""
        for file_path, file_data in files_dict.items():
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
            pass
    
    def _parse_js_imports(self, file_path: str, content: str):
        """Parse JavaScript/TypeScript imports"""
        import_patterns = [
            r"import\s+.*?\s+from\s+['\"]([^'\"]+)['\"]",
            r"import\s+['\"]([^'\"]+)['\"]",
            r"require\(['\"]([^'\"]+)['\"]\)"
        ]
        
        for pattern in import_patterns:
            matches = re.findall(pattern, content)
            for match in matches:
                if not match.startswith('.'):
                    self._add_dependency(file_path, match, 'import')
    
    def _add_dependency(self, source_file: str, target_module: str, dep_type: str):
        """Add dependency edge to graph"""
        if source_file != target_module:
            self.graph.add_edge(
                source_file, 
                target_module, 
                type=dep_type,
                weight=1
            )
    
    def _calculate_centrality_metrics(self):
        """Calculate centrality metrics for all nodes"""
        if not self.graph.nodes():
            return
        
        # Calculate centrality measures
        try:
            degree_centrality = nx.degree_centrality(self.graph)
            betweenness_centrality = nx.betweenness_centrality(self.graph)
            closeness_centrality = nx.closeness_centrality(self.graph)
            
            # Update node attributes
            for node in self.graph.nodes():
                self.graph.nodes[node]['degree'] = degree_centrality.get(node, 0)
                self.graph.nodes[node]['betweenness'] = betweenness_centrality.get(node, 0)
                self.graph.nodes[node]['centrality'] = closeness_centrality.get(node, 0)
        except:
            pass
    
    def _generate_dependency_metrics(self) -> Dict:
        """Generate comprehensive dependency metrics"""
        if not self.graph.nodes():
            return {}
        
        metrics = {
            'total_files': len(self.graph.nodes()),
            'total_dependencies': len(self.graph.edges()),
            'average_dependencies_per_file': len(self.graph.edges()) / len(self.graph.nodes()) if self.graph.nodes() else 0,
            'most_connected_file': None,
            'most_central_file': None,
            'circular_dependencies': [],
            'orphaned_files': [],
            'language_distribution': {},
            'complexity_distribution': {},
            'dependency_depth': 0
        }
        
        # Find most connected file
        if self.graph.nodes():
            degrees = dict(self.graph.degree())
            if degrees:
                metrics['most_connected_file'] = max(degrees, key=degrees.get)
        
        # Find most central file
        centralities = {node: data.get('centrality', 0) for node, data in self.graph.nodes(data=True)}
        if centralities:
            metrics['most_central_file'] = max(centralities, key=centralities.get)
        
        # Find circular dependencies
        try:
            cycles = list(nx.simple_cycles(self.graph))
            metrics['circular_dependencies'] = cycles[:5]
        except:
            pass
        
        # Find orphaned files
        orphaned = [node for node in self.graph.nodes() if self.graph.degree(node) == 0]
        metrics['orphaned_files'] = orphaned[:10]
        
        # Language distribution
        languages = [data.get('language', 'unknown') for _, data in self.graph.nodes(data=True)]
        metrics['language_distribution'] = dict(Counter(languages))
        
        # Complexity distribution
        complexities = [data.get('complexity', 0) for _, data in self.graph.nodes(data=True)]
        metrics['complexity_distribution'] = {
            'low': len([c for c in complexities if c <= 5]),
            'medium': len([c for c in complexities if 5 < c <= 15]),
            'high': len([c for c in complexities if c > 15])
        }
        
        # Calculate dependency depth
        try:
            metrics['dependency_depth'] = nx.dag_longest_path_length(self.graph) if nx.is_directed_acyclic_graph(self.graph) else 0
        except:
            metrics['dependency_depth'] = 0
        
        return metrics
    
    def create_network_graph(self) -> go.Figure:
        """Create neural network-style interactive dependency graph with enhanced visibility"""
        if not self.graph.nodes():
            return go.Figure()
        
        # Calculate layout with better spacing
        pos = nx.spring_layout(self.graph, k=5, iterations=100, seed=42)
        
        # Prepare edge data with gradient effects
        edge_x = []
        edge_y = []
        edge_info = []
        edge_colors = []
        edge_widths = []
        
        for edge in self.graph.edges():
            x0, y0 = pos[edge[0]]
            x1, y1 = pos[edge[1]]
            edge_x.extend([x0, x1, None])
            edge_y.extend([y0, y1, None])
            edge_info.append(f"{Path(edge[0]).name} → {Path(edge[1]).name}")
            
            # Dynamic edge styling based on connection strength
            weight = self.graph[edge[0]][edge[1]].get('weight', 1)
            edge_widths.append(max(1, min(5, weight * 2)))
            edge_colors.append(f'rgba(102, 126, 234, {0.3 + weight * 0.4})')
        
        # Create edge trace with neural network styling
        edge_trace = go.Scatter(
            x=edge_x, y=edge_y,
            line=dict(width=2, color='rgba(102, 126, 234, 0.6)'),
            hoverinfo='none',
            mode='lines',
            name='Dependencies',
            showlegend=False,
            opacity=0.8
        )
        
        # Prepare node data with neural network styling
        node_x = []
        node_y = []
        node_text = []
        node_info = []
        node_colors = []
        node_sizes = []
        node_border_colors = []
        node_border_widths = []
        
        for node in self.graph.nodes():
            x, y = pos[node]
            node_x.append(x)
            node_y.append(y)
            
            node_data = self.graph.nodes[node]
            file_name = Path(node).name
            
            node_text.append(file_name)
            node_info.append(f"""
            <div style='background: rgba(0,0,0,0.8); padding: 10px; border-radius: 8px; color: white;'>
                <b style='color: #4ecdc4; font-size: 14px;'>{file_name}</b><br><br>
                <b>Language:</b> <span style='color: #ffd93d;'>{node_data.get('language', 'unknown')}</span><br>
                <b>SLOC:</b> <span style='color: #6bcf7f;'>{node_data.get('sloc', 0)}</span><br>
                <b>Complexity:</b> <span style='color: #ff6b6b;'>{node_data.get('complexity', 0)}</span><br>
                <b>Imports:</b> <span style='color: #4ecdc4;'>{node_data.get('imports_count', 0)}</span><br>
                <b>Connections:</b> <span style='color: #ffd93d;'>{self.graph.degree(node)}</span><br>
                <b>Centrality:</b> <span style='color: #6bcf7f;'>{node_data.get('centrality', 0):.3f}</span>
            </div>
            """)
            
            # Enhanced color scheme with better contrast
            lang_colors = {
                'python': '#3776ab',
                'javascript': '#f7df1e', 
                'typescript': '#3178c6',
                'unknown': '#6c757d'
            }
            node_colors.append(lang_colors.get(node_data.get('language', 'unknown'), '#6c757d'))
            
            # Neural network-style sizing
            centrality = node_data.get('centrality', 0)
            connections = self.graph.degree(node)
            size = max(20, min(60, 25 + centrality * 40 + connections * 3))
            node_sizes.append(size)
            
            # Dynamic border styling
            if connections > 5:
                node_border_colors.append('#ff6b6b')  # High connectivity - red border
                node_border_widths.append(3)
            elif centrality > 0.5:
                node_border_colors.append('#4ecdc4')  # High centrality - teal border
                node_border_widths.append(2)
            else:
                node_border_colors.append('#ffffff')  # Normal - white border
                node_border_widths.append(1)
        
        # Create node trace with neural network styling
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
                line=dict(
                    width=node_border_widths, 
                    color=node_border_colors
                ),
                opacity=0.9,
                symbol='circle'
            ),
            name='Files',
            hovertemplate='%{hovertext}<extra></extra>'
        )
        
        # Create figure with neural network theme
        fig = go.Figure(data=[edge_trace, node_trace],
                       layout=go.Layout(
                           title=dict(
                               text='🧠 Neural Network-Style Code Dependencies',
                               font=dict(size=24, color='#ffffff', family='Arial Black'),
                               x=0.5,
                               y=0.95
                           ),
                           showlegend=True,
                           hovermode='closest',
                           margin=dict(b=40, l=20, r=20, t=80),
                           annotations=[
                               dict(
                                   text="🔍 Hover for details • 🖱️ Drag to explore • 🔍 Zoom to focus",
                                   showarrow=False,
                                   xref="paper", yref="paper",
                                   x=0.5, y=-0.1,
                                   xanchor='center', yanchor='top',
                                   font=dict(color='#4ecdc4', size=14, family='Arial')
                               ),
                               dict(
                                   text="💡 Node size = Centrality + Connections • Color = Language • Border = Importance",
                                   showarrow=False,
                                   xref="paper", yref="paper",
                                   x=0.5, y=-0.15,
                                   xanchor='center', yanchor='top',
                                   font=dict(color='#ffd93d', size=12, family='Arial')
                               )
                           ],
                           xaxis=dict(
                               showgrid=True, 
                               gridcolor='rgba(255,255,255,0.1)',
                               zeroline=False, 
                               showticklabels=False,
                               range=[-1.2, 1.2]
                           ),
                           yaxis=dict(
                               showgrid=True, 
                               gridcolor='rgba(255,255,255,0.1)',
                               zeroline=False, 
                               showticklabels=False,
                               range=[-1.2, 1.2]
                           ),
                           plot_bgcolor='rgba(0,0,0,0.8)',
                           paper_bgcolor='rgba(0,0,0,0)',
                           font=dict(color='#ffffff', family='Arial'),
                           width=800,
                           height=600
                       ))
        
        return fig
    
    def create_dependency_sunburst(self) -> go.Figure:
        """Create enhanced sunburst chart for dependency hierarchy with better visibility"""
        if not self.graph.nodes():
            return go.Figure()
        
        # Build hierarchy using only real file nodes (typed during graph build)
        hierarchy = defaultdict(list)
        file_nodes: list[str] = []
        for node, data in self.graph.nodes(data=True):
            if data.get('type') == 'file':
                file_nodes.append(node)
                parts = Path(node).parts
                if len(parts) > 1:
                    parent = str(Path(*parts[:-1])) or 'root'
                    hierarchy[parent].append(node)
                else:
                    hierarchy['root'].append(node)
        
        # If no proper file structure, create a simple hierarchy
        if not hierarchy or len(hierarchy.get('root', [])) == 0:
            # Create a simple flat structure
            ids = ['root']
            labels = ['📁 Repository']
            parents = ['']
            values = [0]  # computed from children
            colors = ['#667eea']
            
            child_sum = 0
            for i, node in enumerate(file_nodes[:30]):  # show up to 30 files for visibility
                node_name = Path(node).name
                ids.append(f'file_{i}')
                labels.append(node_name)
                parents.append('root')
                
                # Value based on connections
                connections = self.graph.degree(node)
                val = max(1, connections)
                values.append(val)
                child_sum += val
                
                # Color based on file type
                if node.endswith('.py'):
                    colors.append('#3776ab')
                elif node.endswith(('.js', '.ts')):
                    colors.append('#f7df1e')
                else:
                    colors.append('#6c757d')
            values[0] = child_sum
        else:
            # Create proper hierarchy
            ids = ['root']
            labels = ['📁 Repository']
            parents = ['']
            values = [0]  # computed from children
            colors = ['#667eea']
            
            # Add directories as children of their own parent directory (multi-level)
            dir_nodes = set(k for k in hierarchy.keys() if k != 'root')
            # Ensure parent dirs exist
            for d in list(dir_nodes):
                cur = Path(d)
                while True:
                    parent_dir = str(cur.parent) if str(cur.parent) != '.' else 'root'
                    if parent_dir != 'root' and parent_dir not in dir_nodes:
                        dir_nodes.add(parent_dir)
                        cur = Path(parent_dir)
                        continue
                    break
            dir_nodes = sorted(dir_nodes, key=lambda p: (len(Path(p).parts), p))

            id_index: dict[str, int] = {'root': 0}
            for d in dir_nodes:
                parent_dir = str(Path(d).parent) if str(Path(d).parent) != '.' else 'root'
                ids.append(d)
                labels.append(f"📂 {Path(d).name or 'root'}")
                parents.append(parent_dir if parent_dir in id_index or parent_dir == 'root' else 'root')
                values.append(0)  # will be filled from children
                colors.append('#764ba2')
                id_index[d] = len(ids) - 1
            
            # Add files
            root_sum = 0
            for parent, children in hierarchy.items():
                dir_sum = 0
                for child in children[:50]:  # reasonable cap per directory
                    child_name = Path(child).name
                    ids.append(child)
                    labels.append(child_name)
                    # map to closest existing directory id
                    parents.append(parent if parent in id_index or parent == 'root' else 'root')
                    
                    # Value based on connections
                    connections = self.graph.degree(child)
                    val = max(1, connections)
                    values.append(val)
                    dir_sum += val
                    
                    # Color based on file type
                    if child.endswith('.py'):
                        colors.append('#3776ab')
                    elif child.endswith(('.js', '.ts')):
                        colors.append('#f7df1e')
                    else:
                        colors.append('#6c757d')
                if parent in id_index:
                    values[id_index[parent]] = dir_sum
                    root_sum += dir_sum
            values[0] = max(values[0], root_sum)
        
        # Create enhanced sunburst with proper data structure
        fig = go.Figure(go.Sunburst(
            ids=ids,
            labels=labels,
            parents=parents,
            values=values,
            branchvalues="total",
            hovertemplate='<div style="background: rgba(0,0,0,0.9); padding: 12px; border-radius: 10px; color: white; border: 1px solid #4ecdc4;">' +
                         '<b style="color: #4ecdc4; font-size: 16px;">%{label}</b><br><br>' +
                         '<b>Connections:</b> <span style="color: #ffd93d;">%{value}</span><br>' +
                         '<b>Percentage:</b> <span style="color: #6bcf7f;">%{percentParent}</span><br>' +
                         '<b>Path:</b> <span style="color: #ff6b6b;">%{id}</span>' +
                         '</div><extra></extra>',
            marker=dict(
                colors=colors,
                line=dict(width=2, color='rgba(255,255,255,0.9)'),
                pattern=dict(fillmode="overlay", size=8, solidity=0.3)
            ),
            maxdepth=4,
            textinfo='label+value',
            textfont=dict(size=14, color='white', family='Arial Bold'),
            insidetextorientation='horizontal',
            rotation=0
        ))
        
        fig.update_layout(
            title=dict(
                text='🌞 Enhanced Dependency Hierarchy',
                font=dict(size=20, color='#ffffff', family='Arial Black'),
                x=0.5,
                y=0.92
            ),
            font=dict(color='#ffffff', family='Arial', size=12),
            plot_bgcolor='rgba(0,0,0,0.9)',
            paper_bgcolor='rgba(0,0,0,0)',
            margin=dict(t=80, b=40, l=40, r=40),
            width=900,
            height=800,
            annotations=[
                dict(
                    text="🔍 Click to drill down • 🖱️ Hover for details • 📊 Size = Connections + Complexity",
                    showarrow=False,
                    xref="paper", yref="paper",
                    x=0.5, y=-0.12,
                    xanchor='center', yanchor='top',
                    font=dict(color='#4ecdc4', size=12, family='Arial'),
                    bgcolor='rgba(0,0,0,0.7)',
                    bordercolor='#4ecdc4',
                    borderwidth=1,
                    borderpad=6
                )
            ]
        )
        
        return fig
    
    def create_dependency_heatmap(self) -> go.Figure:
        """Create enhanced dependency heatmap matrix with better visibility"""
        if not self.graph.nodes():
            return go.Figure()
        
        # Create adjacency matrix with weights
        nodes = list(self.graph.nodes())
        matrix = np.zeros((len(nodes), len(nodes)))
        
        for i, node1 in enumerate(nodes):
            for j, node2 in enumerate(nodes):
                if self.graph.has_edge(node1, node2):
                    weight = self.graph[node1][node2].get('weight', 1)
                    matrix[i][j] = weight
        
        # Create enhanced heatmap
        fig = go.Figure(data=go.Heatmap(
            z=matrix,
            x=[Path(node).name for node in nodes],
            y=[Path(node).name for node in nodes],
            colorscale=[
                [0, 'rgba(0,0,0,0)'],
                [0.1, 'rgba(102, 126, 234, 0.3)'],
                [0.5, 'rgba(102, 126, 234, 0.7)'],
                [1, 'rgba(102, 126, 234, 1)']
            ],
            hoverongaps=False,
            hovertemplate='<div style="background: rgba(0,0,0,0.8); padding: 10px; border-radius: 8px; color: white;">' +
                         '<b style="color: #4ecdc4; font-size: 14px;">%{y} → %{x}</b><br><br>' +
                         '<b>Dependency Strength:</b> <span style="color: #ffd93d;">%{z}</span><br>' +
                         '<b>Type:</b> <span style="color: #6bcf7f;">Direct Import</span>' +
                         '</div><extra></extra>',
            showscale=True,
            colorbar=dict(
                title=dict(
                    text="Dependency Strength",
                    font=dict(color='white', size=14)
                ),
                tickfont=dict(color='white'),
                bgcolor='rgba(0,0,0,0.5)',
                bordercolor='white',
                borderwidth=1
            )
        ))
        
        fig.update_layout(
            title=dict(
                text='🔥 Enhanced Dependency Matrix',
                font=dict(size=20, color='#ffffff', family='Arial Black'),
                x=0.5,
                y=0.92
            ),
            xaxis=dict(
                title=dict(text='Dependencies (Target Files)', font=dict(color='#4ecdc4', size=14, family='Arial Bold')),
                tickfont=dict(color='white', size=10, family='Arial'),
                showgrid=True,
                gridcolor='rgba(255,255,255,0.2)',
                gridwidth=1,
                zeroline=False,
                showline=True,
                linecolor='rgba(255,255,255,0.3)',
                linewidth=1
            ),
            yaxis=dict(
                title=dict(text='Files (Source)', font=dict(color='#4ecdc4', size=14, family='Arial Bold')),
                tickfont=dict(color='white', size=10, family='Arial'),
                showgrid=True,
                gridcolor='rgba(255,255,255,0.2)',
                gridwidth=1,
                zeroline=False,
                showline=True,
                linecolor='rgba(255,255,255,0.3)',
                linewidth=1
            ),
            font=dict(color='#ffffff', family='Arial'),
            plot_bgcolor='rgba(0,0,0,0.9)',
            paper_bgcolor='rgba(0,0,0,0)',
            height=max(700, len(nodes) * 35),
            width=max(900, len(nodes) * 35),
            margin=dict(t=120, b=120, l=120, r=80),
            annotations=[
                dict(
                    text="🔍 Hover for details • 📊 Blue intensity = Dependency strength • ⚪ White = No dependency",
                    showarrow=False,
                    xref="paper", yref="paper",
                    x=0.5, y=-0.1,
                    xanchor='center', yanchor='top',
                    font=dict(color='#4ecdc4', size=12, family='Arial'),
                    bgcolor='rgba(0,0,0,0.7)',
                    bordercolor='#4ecdc4',
                    borderwidth=1,
                    borderpad=6
                )
            ]
        )
        
        return fig
    
    def create_centrality_analysis(self) -> go.Figure:
        """Create enhanced centrality analysis chart with better visibility"""
        if not self.graph.nodes():
            return go.Figure()
        
        # Prepare data with enhanced metrics
        nodes = []
        degrees = []
        centralities = []
        betweenness = []
        languages = []
        complexities = []
        
        for node in self.graph.nodes():
            node_data = self.graph.nodes[node]
            nodes.append(Path(node).name)
            degrees.append(self.graph.degree(node))
            centralities.append(node_data.get('centrality', 0))
            betweenness.append(node_data.get('betweenness', 0))
            languages.append(node_data.get('language', 'unknown'))
            complexities.append(node_data.get('complexity', 0))
        
        # Create enhanced subplot with proper separation
        fig = make_subplots(
            rows=2, cols=2,
            subplot_titles=(
                '🔗 Degree Centrality', 
                '🎯 Closeness Centrality', 
                '⚡ Betweenness Centrality', 
                '📊 Language Distribution'
            ),
            specs=[[{"type": "bar"}, {"type": "bar"}],
                   [{"type": "bar"}, {"type": "pie"}]],
            vertical_spacing=0.2,
            horizontal_spacing=0.2
        )
        
        # Enhanced degree centrality with gradient (no overlapping colorbars)
        fig.add_trace(
            go.Bar(
                x=nodes, 
                y=degrees, 
                name='Degree',
                marker=dict(
                    color=degrees,
                    colorscale='Viridis',
                    showscale=False,
                    line=dict(width=1, color='white')
                ),
                hovertemplate='<div style="background: rgba(0,0,0,0.8); padding: 10px; border-radius: 8px; color: white;">' +
                             '<b style="color: #4ecdc4;">%{x}</b><br>' +
                             '<b>Connections:</b> <span style="color: #ffd93d;">%{y}</span>' +
                             '</div><extra></extra>',
                width=0.6
            ),
            row=1, col=1
        )
        
        # Enhanced closeness centrality
        fig.add_trace(
            go.Bar(
                x=nodes, 
                y=centralities, 
                name='Closeness',
                marker=dict(
                    color=centralities,
                    colorscale='Plasma',
                    showscale=False,
                    line=dict(width=1, color='white')
                ),
                hovertemplate='<div style="background: rgba(0,0,0,0.8); padding: 10px; border-radius: 8px; color: white;">' +
                             '<b style="color: #4ecdc4;">%{x}</b><br>' +
                             '<b>Closeness:</b> <span style="color: #ffd93d;">%{y:.3f}</span>' +
                             '</div><extra></extra>',
                width=0.6
            ),
            row=1, col=2
        )
        
        # Enhanced betweenness centrality
        fig.add_trace(
            go.Bar(
                x=nodes, 
                y=betweenness, 
                name='Betweenness',
                marker=dict(
                    color=betweenness,
                    colorscale='Inferno',
                    showscale=False,
                    line=dict(width=1, color='white')
                ),
                hovertemplate='<div style="background: rgba(0,0,0,0.8); padding: 10px; border-radius: 8px; color: white;">' +
                             '<b style="color: #4ecdc4;">%{x}</b><br>' +
                             '<b>Betweenness:</b> <span style="color: #ffd93d;">%{y:.3f}</span>' +
                             '</div><extra></extra>',
                width=0.6
            ),
            row=2, col=1
        )
        
        # Enhanced language distribution
        lang_counts = Counter(languages)
        lang_colors = {
            'python': '#3776ab',
            'javascript': '#f7df1e',
            'typescript': '#3178c6',
            'unknown': '#6c757d'
        }
        pie_colors = [lang_colors.get(lang, '#6c757d') for lang in lang_counts.keys()]
        
        fig.add_trace(
            go.Pie(
                labels=list(lang_counts.keys()), 
                values=list(lang_counts.values()), 
                name='Languages',
                marker=dict(
                    colors=pie_colors,
                    line=dict(width=2, color='white')
                ),
                hovertemplate='<div style="background: rgba(0,0,0,0.8); padding: 10px; border-radius: 8px; color: white;">' +
                             '<b style="color: #4ecdc4;">%{label}</b><br>' +
                             '<b>Files:</b> <span style="color: #ffd93d;">%{value}</span><br>' +
                             '<b>Percentage:</b> <span style="color: #6bcf7f;">%{percent}</span>' +
                             '</div><extra></extra>'
            ),
            row=2, col=2
        )
        
        # Update layout with enhanced styling and proper separation
        fig.update_layout(
            title=dict(
                text='📊 Enhanced Centrality Analysis Dashboard',
                font=dict(size=20, color='#ffffff', family='Arial Black'),
                x=0.5,
                y=0.95
            ),
            showlegend=False,
            font=dict(color='#ffffff', family='Arial'),
            plot_bgcolor='rgba(0,0,0,0.9)',
            paper_bgcolor='rgba(0,0,0,0)',
            height=850,
            width=1280,
            margin=dict(t=90, b=120, l=70, r=40),
            annotations=[
                dict(
                    text="🔍 Hover for detailed metrics • 📊 Color intensity = Value magnitude • 🎯 Higher values = More important files",
                    showarrow=False,
                    xref="paper", yref="paper",
                    x=0.5, y=-0.12,
                    xanchor='center', yanchor='top',
                    font=dict(color='#4ecdc4', size=12, family='Arial'),
                    bgcolor='rgba(0,0,0,0.7)',
                    bordercolor='#4ecdc4',
                    borderwidth=1,
                    borderpad=6
                )
            ]
        )
        
        # Update subplot titles with better styling
        for i, title in enumerate(['Degree Centrality', 'Closeness Centrality', 'Betweenness Centrality', 'Language Distribution']):
            fig.layout.annotations[i].update(
                font=dict(color='#4ecdc4', size=16, family='Arial Bold'),
                bgcolor='rgba(0,0,0,0.8)',
                bordercolor='#4ecdc4',
                borderwidth=1,
                borderpad=8
            )
        
        # Update axes styling for better separation
        fig.update_xaxes(
            showgrid=True,
            gridcolor='rgba(255,255,255,0.1)',
            gridwidth=1,
            zeroline=False,
            showline=True,
            linecolor='rgba(255,255,255,0.3)',
            linewidth=1,
            tickfont=dict(color='white', size=10, family='Arial')
        )
        
        fig.update_yaxes(
            showgrid=True,
            gridcolor='rgba(255,255,255,0.1)',
            gridwidth=1,
            zeroline=False,
            showline=True,
            linecolor='rgba(255,255,255,0.3)',
            linewidth=1,
            tickfont=dict(color='white', size=10, family='Arial')
        )
        
        return fig
    
    def create_dependency_metrics_cards(self) -> Dict:
        """Create metrics cards data"""
        metrics = self.dependency_metrics
        
        cards = [
            {
                'title': 'Total Files',
                'value': metrics.get('total_files', 0),
                'icon': '📁',
                'color': '#667eea'
            },
            {
                'title': 'Dependencies',
                'value': metrics.get('total_dependencies', 0),
                'icon': '🔗',
                'color': '#764ba2'
            },
            {
                'title': 'Avg Dependencies/File',
                'value': f"{metrics.get('average_dependencies_per_file', 0):.1f}",
                'icon': '📊',
                'color': '#f093fb'
            },
            {
                'title': 'Most Connected',
                'value': Path(metrics.get('most_connected_file', 'N/A')).name if metrics.get('most_connected_file') else 'N/A',
                'icon': '⭐',
                'color': '#4ecdc4'
            },
            {
                'title': 'Circular Deps',
                'value': len(metrics.get('circular_dependencies', [])),
                'icon': '🔄',
                'color': '#ff6b6b'
            },
            {
                'title': 'Orphaned Files',
                'value': len(metrics.get('orphaned_files', [])),
                'icon': '🏝️',
                'color': '#ffa726'
            }
        ]
        
        return cards


def create_advanced_dependency_visualizations(repo_data: Dict) -> Dict:
    """Main function to create all advanced dependency visualizations"""
    visualizer = AdvancedDependencyVisualizer()
    analysis = visualizer.build_advanced_dependency_graph(repo_data)
    
    visualizations = {
        'network_graph': visualizer.create_network_graph(),
        'sunburst': visualizer.create_dependency_sunburst(),
        'heatmap': visualizer.create_dependency_heatmap(),
        'centrality_analysis': visualizer.create_centrality_analysis(),
        'metrics_cards': visualizer.create_dependency_metrics_cards(),
        'metrics': analysis['dependency_metrics']
    }
    
    return visualizations
