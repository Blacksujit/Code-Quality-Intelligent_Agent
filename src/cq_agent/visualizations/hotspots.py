"""
Code Hotspots Heatmap Visualization
Creates interactive heatmaps showing code complexity, churn, and issue density
"""

import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np
from typing import Dict, List, Tuple
from pathlib import Path


class HotspotVisualizer:
    """Creates interactive code hotspot visualizations"""
    
    def __init__(self):
        self.hotspot_data = []
        self.file_metrics = {}
    
    def analyze_hotspots(self, repo_data: Dict, hotspots: List[Tuple]) -> Dict:
        """Analyze code hotspots and prepare visualization data"""
        self.hotspot_data = hotspots
        self.file_metrics = {}
        
        # Handle both RepoContext and dict formats
        if hasattr(repo_data, 'files'):
            files_dict = repo_data.files
        else:
            files_dict = repo_data.get('files', {})
        
        # Process each file for hotspot analysis
        for file_path, file_data in files_dict.items():
            self._analyze_file_hotspots(file_path, file_data)
        
        return self._create_hotspot_metrics()
    
    def _analyze_file_hotspots(self, file_path: str, file_data: Dict):
        """Analyze hotspots for a single file"""
        # Handle both FileRecord and dict formats
        if hasattr(file_data, 'sloc'):
            sloc = file_data.sloc
            churn = 0  # Will be calculated from git data
            issues = []  # Will be passed separately
            complexity = 0  # Will be calculated
        else:
            sloc = file_data.get('sloc', 0)
            churn = file_data.get('churn', 0)
            issues = file_data.get('issues', [])
            complexity = file_data.get('complexity', 0)
        
        # Calculate hotspot score
        hotspot_score = self._calculate_hotspot_score(sloc, churn, len(issues), complexity)
        
        # Calculate issue density per line
        issue_density = len(issues) / max(sloc, 1)
        
        # Calculate complexity per line
        complexity_density = complexity / max(sloc, 1)
        
        self.file_metrics[file_path] = {
            'file_path': file_path,
            'file_name': Path(file_path).name,
            'directory': str(Path(file_path).parent),
            'sloc': sloc,
            'churn': churn,
            'issues_count': len(issues),
            'complexity': complexity,
            'hotspot_score': hotspot_score,
            'issue_density': issue_density,
            'complexity_density': complexity_density,
            'language': file_data.get('language', 'unknown'),
            'severity_breakdown': self._analyze_severity_breakdown(issues)
        }
    
    def _calculate_hotspot_score(self, sloc: int, churn: int, issues_count: int, complexity: int) -> float:
        """Calculate comprehensive hotspot score"""
        # Normalize metrics (0-1 scale)
        sloc_norm = min(sloc / 1000, 1.0)  # Cap at 1000 lines
        churn_norm = min(churn / 100, 1.0)  # Cap at 100 changes
        issues_norm = min(issues_count / 50, 1.0)  # Cap at 50 issues
        complexity_norm = min(complexity / 50, 1.0)  # Cap at 50 complexity
        
        # Weighted combination
        hotspot_score = (
            sloc_norm * 0.2 +      # Size matters
            churn_norm * 0.3 +     # Churn is critical
            issues_norm * 0.3 +    # Issues are important
            complexity_norm * 0.2  # Complexity adds risk
        )
        
        return round(hotspot_score, 3)
    
    def _analyze_severity_breakdown(self, issues: List[Dict]) -> Dict:
        """Analyze severity breakdown of issues"""
        severity_counts = {'critical': 0, 'high': 0, 'medium': 0, 'low': 0}
        
        for issue in issues:
            severity = issue.get('severity', 'low')
            if severity in severity_counts:
                severity_counts[severity] += 1
        
        return severity_counts
    
    def _create_hotspot_metrics(self) -> Dict:
        """Create comprehensive hotspot metrics"""
        if not self.file_metrics:
            return {}
        
        df = pd.DataFrame(list(self.file_metrics.values()))
        
        return {
            'total_files': len(df),
            'high_hotspot_files': len(df[df['hotspot_score'] > 0.7]),
            'medium_hotspot_files': len(df[(df['hotspot_score'] > 0.4) & (df['hotspot_score'] <= 0.7)]),
            'low_hotspot_files': len(df[df['hotspot_score'] <= 0.4]),
            'average_hotspot_score': df['hotspot_score'].mean(),
            'max_hotspot_score': df['hotspot_score'].max(),
            'most_complex_file': df.loc[df['complexity'].idxmax(), 'file_path'] if not df.empty else None,
            'most_churned_file': df.loc[df['churn'].idxmax(), 'file_path'] if not df.empty else None,
            'most_issues_file': df.loc[df['issues_count'].idxmax(), 'file_path'] if not df.empty else None
        }
    
    def create_hotspot_heatmap(self) -> go.Figure:
        """Create interactive hotspot heatmap"""
        if not self.file_metrics:
            return go.Figure()
        
        df = pd.DataFrame(list(self.file_metrics.values()))
        
        # Group by directory for heatmap
        df['directory_depth'] = df['directory'].apply(lambda x: len(Path(x).parts))
        df['dir_name'] = df['directory'].apply(lambda x: Path(x).name or 'root')
        
        # Create pivot table for heatmap
        heatmap_data = df.groupby(['dir_name', 'language'])['hotspot_score'].mean().unstack(fill_value=0)
        
        # Create heatmap
        fig = go.Figure(data=go.Heatmap(
            z=heatmap_data.values,
            x=heatmap_data.columns,
            y=heatmap_data.index,
            colorscale='Reds',
            hoverongaps=False,
            hovertemplate='<b>%{y}</b><br>Language: %{x}<br>Hotspot Score: %{z:.3f}<extra></extra>',
            colorbar=dict(title="Hotspot Score")
        ))
        
        fig.update_layout(
            title='Code Hotspots Heatmap by Directory and Language',
            xaxis_title='Programming Language',
            yaxis_title='Directory',
            font=dict(size=12),
            height=max(400, len(heatmap_data) * 30)
        )
        
        return fig
    
    def create_hotspot_scatter(self) -> go.Figure:
        """Create interactive scatter plot of hotspots"""
        if not self.file_metrics:
            return go.Figure()
        
        df = pd.DataFrame(list(self.file_metrics.values()))
        
        # Create scatter plot
        fig = px.scatter(
            df, 
            x='sloc', 
            y='hotspot_score',
            size='issues_count',
            color='complexity',
            hover_data=['file_name', 'churn', 'issue_density'],
            color_continuous_scale='Viridis',
            title='Code Hotspots: Size vs Score vs Issues vs Complexity'
        )
        
        fig.update_layout(
            xaxis_title='Lines of Code (SLOC)',
            yaxis_title='Hotspot Score',
            font=dict(size=12)
        )
        
        # Add trend line
        if len(df) > 1:
            z = np.polyfit(df['sloc'], df['hotspot_score'], 1)
            p = np.poly1d(z)
            fig.add_trace(go.Scatter(
                x=df['sloc'],
                y=p(df['sloc']),
                mode='lines',
                name='Trend',
                line=dict(dash='dash', color='red')
            ))
        
        return fig
    
    def create_language_comparison(self) -> go.Figure:
        """Create language comparison chart"""
        if not self.file_metrics:
            return go.Figure()
        
        df = pd.DataFrame(list(self.file_metrics.values()))
        
        # Group by language
        lang_stats = df.groupby('language').agg({
            'hotspot_score': ['mean', 'std', 'count'],
            'sloc': 'mean',
            'issues_count': 'mean',
            'complexity': 'mean'
        }).round(3)
        
        # Flatten column names
        lang_stats.columns = ['_'.join(col).strip() for col in lang_stats.columns]
        lang_stats = lang_stats.reset_index()
        
        # Create radar chart
        categories = ['hotspot_score_mean', 'sloc_mean', 'issues_count_mean', 'complexity_mean']
        
        fig = go.Figure()
        
        for _, row in lang_stats.iterrows():
            values = [row[cat] for cat in categories]
            # Normalize values for radar chart
            max_vals = lang_stats[categories].max()
            normalized_values = [v / max(max_vals[cat], 1) for v, cat in zip(values, categories)]
            
            fig.add_trace(go.Scatterpolar(
                r=normalized_values,
                theta=['Hotspot Score', 'Avg SLOC', 'Avg Issues', 'Avg Complexity'],
                fill='toself',
                name=row['language'],
                line=dict(width=2)
            ))
        
        fig.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[0, 1]
                )),
            showlegend=True,
            title="Language Comparison - Code Quality Metrics"
        )
        
        return fig
    
    def create_treemap(self) -> go.Figure:
        """Create treemap visualization of hotspots (size=SLOC, color=hotspot)"""
        if not self.file_metrics:
            return go.Figure()
        
        df = pd.DataFrame(list(self.file_metrics.values()))
        if df.empty:
            return go.Figure()
        
        # Normalize directory paths and ensure root
        df['directory'] = df['directory'].apply(lambda d: d if d else 'root')
        df['parent_dir'] = df['directory'].apply(lambda d: str(Path(d).parent) if str(Path(d).parent) not in ('', '.') else 'root')
        
        # Construct file ids (unique) and collect directories
        df['file_id'] = df['directory'].astype(str) + '/' + df['file_name'].astype(str)
        all_dirs = set(df['directory']) | set(df['parent_dir'])
        if '' in all_dirs:
            all_dirs.remove('')
        all_dirs.add('root')

        # Build directory hierarchy ensuring parents exist
        dir_rows = []
        for d in sorted(all_dirs, key=lambda p: (len(Path(p).parts), p)):
            parent = str(Path(d).parent) if str(Path(d).parent) not in ('', '.') else ''
            if d == 'root':
                parent = ''
            dir_rows.append({
                'id': d,
                'label': Path(d).name or 'root',
                'parent': parent if parent in all_dirs or parent == '' else '',
                'value': 0.0
            })

        # File nodes reference their directory ids
        file_rows = []
        for _, row in df.iterrows():
            file_rows.append({
                'id': row['file_id'],
                'label': row['file_name'],
                'parent': row['directory'] if row['directory'] else 'root',
                'value': max(1, int(row['sloc'] or 1)),
                'color': float(row['hotspot_score'])
            })

        # Aggregate directory values as sum of children
        dir_value = {r['id']: 0.0 for r in dir_rows}
        for fr in file_rows:
            dir_value[fr['parent']] = dir_value.get(fr['parent'], 0.0) + float(fr['value'])
        for r in dir_rows:
            if r['id'] != 'root':
                r['value'] = dir_value.get(r['id'], 0.0)
        # Root gets sum of top-level dirs
        rsum = 0.0
        for r in dir_rows:
            if r['parent'] == '' and r['id'] != 'root':
                rsum += r['value']
        for r in dir_rows:
            if r['id'] == 'root':
                r['value'] = max(r['value'], rsum)

        # Assemble final lists
        ids = [r['id'] for r in dir_rows] + [r['id'] for r in file_rows]
        labels = [r['label'] for r in dir_rows] + [r['label'] for r in file_rows]
        parents = [r['parent'] for r in dir_rows] + [r['parent'] for r in file_rows]
        values = [r['value'] for r in dir_rows] + [r['value'] for r in file_rows]
        colors = [None for _ in dir_rows] + [r['color'] for r in file_rows]

        fig = go.Figure(go.Treemap(
            ids=ids,
            labels=labels,
            parents=parents,
            values=values,
            marker=dict(
                colors=colors,
                colorscale='Reds',
                cmin=0,
                cmax=max(1e-6, float(df['hotspot_score'].max()))
            ),
            branchvalues='total',
            textinfo='label+value',
            hovertemplate='<b>%{label}</b><br>SLOC: %{value}<br>Dir: %{parent}<extra></extra>'
        ))
        
        fig.update_layout(
            title="Code Hotspots Treemap",
            margin=dict(t=60, b=20, l=20, r=20),
            height=600
        )
        
        return fig


def create_hotspot_visualizations(repo_data: Dict, hotspots: List[Tuple]) -> Dict:
    """Main function to create all hotspot visualizations"""
    try:
        visualizer = HotspotVisualizer()
        metrics = visualizer.analyze_hotspots(repo_data, hotspots)
        
        visualizations = {
            'heatmap': visualizer.create_hotspot_heatmap(),
            'scatter': visualizer.create_hotspot_scatter(),
            'language_comparison': visualizer.create_language_comparison(),
            'treemap': visualizer.create_treemap(),
            'metrics': metrics,
            'file_data': visualizer.file_metrics
        }
        
        return visualizations
    except Exception as e:
        print(f"Error creating hotspot visualizations: {e}")
        # Return empty visualizations
        return {
            'heatmap': go.Figure(),
            'scatter': go.Figure(),
            'language_comparison': go.Figure(),
            'treemap': go.Figure(),
            'metrics': {},
            'file_data': {}
        }
