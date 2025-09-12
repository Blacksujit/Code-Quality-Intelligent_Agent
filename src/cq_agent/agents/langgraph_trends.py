"""
LangGraph-based Intelligent Trend Analysis
Uses LangGraph for multi-step reasoning about code quality trends
"""

from dataclasses import dataclass
import numpy as np
import pandas as pd
from datetime import datetime, timedelta
import json


class TrendAnalysisState(TypedDict):
    """State for trend analysis workflow"""
    repository_data: Dict
    commit_history: List[Dict]
    quality_metrics: Dict
    trend_insights: List[Dict]
    recommendations: List[str]
    confidence_score: float
    current_step: str


@dataclass
class TrendInsight:
    """Represents a trend insight"""
    type: str  # 'improvement', 'decline', 'stability', 'volatility'
    metric: str
    value: float
    trend_direction: str  # 'up', 'down', 'stable'
    confidence: float
    description: str
    recommendation: str


class LangGraphTrendAnalyzer:
    """LangGraph-based trend analyzer for intelligent code quality insights"""
    
    def __init__(self):
        self.workflow_steps = [
            self.analyze_commit_patterns,
            self.extract_quality_metrics,
            self.identify_trends,
            self.generate_insights,
            self.create_recommendations,
            self.calculate_confidence
        ]
    
    def analyze_trends(self, repository_data: Dict, commit_history: List[Dict]) -> Dict:
        """Main trend analysis workflow using LangGraph pattern"""
        state = TrendAnalysisState(
            repository_data=repository_data,
            commit_history=commit_history,
            quality_metrics={},
            trend_insights=[],
            recommendations=[],
            confidence_score=0.0,
            current_step="start"
        )
        
        # Execute workflow steps
        for step in self.workflow_steps:
            state = step(state)
        
        return {
            'insights': state['trend_insights'],
            'recommendations': state['recommendations'],
            'confidence': state['confidence_score'],
            'metrics': state['quality_metrics']
        }
    
    def analyze_commit_patterns(self, state: TrendAnalysisState) -> TrendAnalysisState:
        """Analyze commit patterns and frequency"""
        state['current_step'] = 'analyze_commit_patterns'
        
        commits = state['commit_history']
        if not commits:
            return state
        
        # Calculate commit frequency patterns
        df = pd.DataFrame(commits)
        df['date'] = pd.to_datetime(df['date'])
        df['day_of_week'] = df['date'].dt.dayofweek
        df['hour'] = df['date'].dt.hour
        
        # Daily commit patterns
        daily_commits = df.groupby(df['date'].dt.date).size()
        avg_daily_commits = daily_commits.mean()
        
        # Weekly patterns
        weekly_commits = df.groupby('day_of_week').size()
        weekday_commits = weekly_commits[weekly_commits.index < 5].sum()
        weekend_commits = weekly_commits[weekly_commits.index >= 5].sum()
        
        # Time patterns
        morning_commits = len(df[(df['hour'] >= 9) & (df['hour'] < 12)])
        afternoon_commits = len(df[(df['hour'] >= 12) & (df['hour'] < 17)])
        evening_commits = len(df[(df['hour'] >= 17) & (df['hour'] < 22)])
        
        state['quality_metrics']['commit_patterns'] = {
            'avg_daily_commits': avg_daily_commits,
            'weekday_commits': weekday_commits,
            'weekend_commits': weekend_commits,
            'morning_commits': morning_commits,
            'afternoon_commits': afternoon_commits,
            'evening_commits': evening_commits,
            'total_commits': len(commits)
        }
        
        return state
    
    def extract_quality_metrics(self, state: TrendAnalysisState) -> TrendAnalysisState:
        """Extract quality metrics from commit history"""
        state['current_step'] = 'extract_quality_metrics'
        
        commits = state['commit_history']
        if not commits:
            return state
        
        df = pd.DataFrame(commits)
        
        # Quality score trends
        if 'quality_score' in df.columns:
            quality_scores = df['quality_score'].dropna()
            state['quality_metrics']['quality_trends'] = {
                'current_quality': quality_scores.iloc[-1] if len(quality_scores) > 0 else 0,
                'avg_quality': quality_scores.mean(),
                'quality_volatility': quality_scores.std(),
                'quality_improvement': self._calculate_trend_slope(quality_scores.values)
            }
        
        # Code volume trends
        if 'lines_added' in df.columns and 'lines_removed' in df.columns:
            df['net_lines'] = df['lines_added'] - df['lines_removed']
            net_lines = df['net_lines'].dropna()
            
            state['quality_metrics']['volume_trends'] = {
                'total_lines_added': df['lines_added'].sum(),
                'total_lines_removed': df['lines_removed'].sum(),
                'net_lines_change': net_lines.sum(),
                'avg_lines_per_commit': (df['lines_added'] + df['lines_removed']).mean(),
                'volume_trend': self._calculate_trend_slope(net_lines.values)
            }
        
        # Issue trends
        if 'issues_count' in df.columns:
            issues = df['issues_count'].dropna()
            state['quality_metrics']['issue_trends'] = {
                'current_issues': issues.iloc[-1] if len(issues) > 0 else 0,
                'avg_issues': issues.mean(),
                'issue_trend': self._calculate_trend_slope(issues.values),
                'issue_volatility': issues.std()
            }
        
        # Complexity trends
        if 'complexity_trend' in df.columns:
            complexity = df['complexity_trend'].dropna()
            state['quality_metrics']['complexity_trends'] = {
                'current_complexity': complexity.iloc[-1] if len(complexity) > 0 else 0,
                'avg_complexity': complexity.mean(),
                'complexity_trend': self._calculate_trend_slope(complexity.values),
                'complexity_volatility': complexity.std()
            }
        
        return state
    
    def identify_trends(self, state: TrendAnalysisState) -> TrendAnalysisState:
        """Identify specific trends and patterns"""
        state['current_step'] = 'identify_trends'
        
        insights = []
        metrics = state['quality_metrics']
        
        # Quality trend analysis
        if 'quality_trends' in metrics:
            qt = metrics['quality_trends']
            if qt['quality_improvement'] > 0.01:
                insights.append(TrendInsight(
                    type='improvement',
                    metric='quality_score',
                    value=qt['current_quality'],
                    trend_direction='up',
                    confidence=min(0.9, abs(qt['quality_improvement']) * 10),
                    description=f"Code quality is improving (trend: +{qt['quality_improvement']:.3f})",
                    recommendation="Continue current practices to maintain quality improvement"
                ))
            elif qt['quality_improvement'] < -0.01:
                insights.append(TrendInsight(
                    type='decline',
                    metric='quality_score',
                    value=qt['current_quality'],
                    trend_direction='down',
                    confidence=min(0.9, abs(qt['quality_improvement']) * 10),
                    description=f"Code quality is declining (trend: {qt['quality_improvement']:.3f})",
                    recommendation="Implement quality gates and code review processes"
                ))
            else:
                insights.append(TrendInsight(
                    type='stability',
                    metric='quality_score',
                    value=qt['current_quality'],
                    trend_direction='stable',
                    confidence=0.7,
                    description="Code quality is stable",
                    recommendation="Monitor for any changes and maintain current standards"
                ))
        
        # Volume trend analysis
        if 'volume_trends' in metrics:
            vt = metrics['volume_trends']
            if vt['volume_trend'] > 10:
                insights.append(TrendInsight(
                    type='improvement',
                    metric='code_volume',
                    value=vt['net_lines_change'],
                    trend_direction='up',
                    confidence=0.8,
                    description="Codebase is growing steadily",
                    recommendation="Ensure new code follows quality standards"
                ))
            elif vt['volume_trend'] < -10:
                insights.append(TrendInsight(
                    type='improvement',
                    metric='code_volume',
                    value=vt['net_lines_change'],
                    trend_direction='down',
                    confidence=0.8,
                    description="Codebase is being refactored and cleaned up",
                    recommendation="Continue refactoring efforts while maintaining functionality"
                ))
        
        # Issue trend analysis
        if 'issue_trends' in metrics:
            it = metrics['issue_trends']
            if it['issue_trend'] > 0.5:
                insights.append(TrendInsight(
                    type='decline',
                    metric='issues',
                    value=it['current_issues'],
                    trend_direction='up',
                    confidence=0.8,
                    description="Issue count is increasing",
                    recommendation="Focus on issue resolution and prevention"
                ))
            elif it['issue_trend'] < -0.5:
                insights.append(TrendInsight(
                    type='improvement',
                    metric='issues',
                    value=it['current_issues'],
                    trend_direction='down',
                    confidence=0.8,
                    description="Issue count is decreasing",
                    recommendation="Maintain current issue resolution practices"
                ))
        
        # Complexity trend analysis
        if 'complexity_trends' in metrics:
            ct = metrics['complexity_trends']
            if ct['complexity_trend'] > 1:
                insights.append(TrendInsight(
                    type='decline',
                    metric='complexity',
                    value=ct['current_complexity'],
                    trend_direction='up',
                    confidence=0.7,
                    description="Code complexity is increasing",
                    recommendation="Refactor complex code and break down large functions"
                ))
            elif ct['complexity_trend'] < -1:
                insights.append(TrendInsight(
                    type='improvement',
                    metric='complexity',
                    value=ct['current_complexity'],
                    trend_direction='down',
                    confidence=0.7,
                    description="Code complexity is decreasing",
                    recommendation="Continue refactoring efforts"
                ))
        
        state['trend_insights'] = insights
        return state
    
    def generate_insights(self, state: TrendAnalysisState) -> TrendAnalysisState:
        """Generate high-level insights from trends"""
        state['current_step'] = 'generate_insights'
        
        insights = state['trend_insights']
        if not insights:
            return state
        
        # Categorize insights
        improvements = [i for i in insights if i.type == 'improvement']
        declines = [i for i in insights if i.type == 'decline']
        stable = [i for i in insights if i.type == 'stability']
        
        # Generate summary insights
        summary_insights = []
        
        if len(improvements) > len(declines):
            summary_insights.append({
                'type': 'positive_summary',
                'description': f"Overall positive trends: {len(improvements)} improvements vs {len(declines)} declines",
                'confidence': np.mean([i.confidence for i in improvements]) if improvements else 0
            })
        elif len(declines) > len(improvements):
            summary_insights.append({
                'type': 'negative_summary',
                'description': f"Concerning trends: {len(declines)} declines vs {len(improvements)} improvements",
                'confidence': np.mean([i.confidence for i in declines]) if declines else 0
            })
        else:
            summary_insights.append({
                'type': 'neutral_summary',
                'description': f"Mixed trends: {len(improvements)} improvements, {len(declines)} declines",
                'confidence': 0.5
            })
        
        # Add volatility analysis
        if insights:
            avg_confidence = np.mean([i.confidence for i in insights])
            if avg_confidence < 0.6:
                summary_insights.append({
                    'type': 'volatility',
                    'description': "High volatility in metrics - trends may be unstable",
                    'confidence': 0.7
                })
        
        state['trend_insights'].extend(summary_insights)
        return state
    
    def create_recommendations(self, state: TrendAnalysisState) -> TrendAnalysisState:
        """Create actionable recommendations based on trends"""
        state['current_step'] = 'create_recommendations'
        
        recommendations = []
        insights = state['trend_insights']
        
        # Priority-based recommendations
        high_priority_issues = [i for i in insights if hasattr(i, 'type') and i.type == 'decline' and i.confidence > 0.7]
        improvements = [i for i in insights if hasattr(i, 'type') and i.type == 'improvement']
        
        if high_priority_issues:
            recommendations.append({
                'priority': 'high',
                'category': 'quality_issues',
                'title': 'Address Declining Metrics',
                'description': f"Focus on {len(high_priority_issues)} declining metrics with high confidence",
                'actions': [i.recommendation for i in high_priority_issues]
            })
        
        if improvements:
            recommendations.append({
                'priority': 'medium',
                'category': 'maintain_improvements',
                'title': 'Maintain Positive Trends',
                'description': f"Continue practices that led to {len(improvements)} improvements",
                'actions': [i.recommendation for i in improvements]
            })
        
        # General recommendations based on patterns
        commit_patterns = state['quality_metrics'].get('commit_patterns', {})
        if commit_patterns.get('weekend_commits', 0) > commit_patterns.get('weekday_commits', 0) * 0.3:
            recommendations.append({
                'priority': 'low',
                'category': 'work_life_balance',
                'title': 'Consider Work-Life Balance',
                'description': "High weekend activity may indicate overwork",
                'actions': ["Consider reducing weekend commits", "Implement better planning for weekday work"]
            })
        
        # Quality gate recommendations
        quality_trends = state['quality_metrics'].get('quality_trends', {})
        if quality_trends.get('quality_volatility', 0) > 0.1:
            recommendations.append({
                'priority': 'medium',
                'category': 'process_improvement',
                'title': 'Implement Quality Gates',
                'description': "High quality volatility suggests need for consistent processes",
                'actions': [
                    "Implement automated quality checks",
                    "Add code review requirements",
                    "Set up continuous integration quality gates"
                ]
            })
        
        state['recommendations'] = recommendations
        return state
    
    def calculate_confidence(self, state: TrendAnalysisState) -> TrendAnalysisState:
        """Calculate overall confidence in the analysis"""
        state['current_step'] = 'calculate_confidence'
        
        # Base confidence on data quality and trend consistency
        commits = state['commit_history']
        insights = state['trend_insights']
        
        if not commits:
            state['confidence_score'] = 0.0
            return state
        
        # Data quality factors
        data_quality = min(1.0, len(commits) / 30)  # More commits = higher confidence
        
        # Trend consistency
        if insights:
            avg_confidence = np.mean([getattr(i, 'confidence', 0.5) for i in insights if hasattr(i, 'confidence')])
            trend_consistency = 1.0 - np.std([getattr(i, 'confidence', 0.5) for i in insights if hasattr(i, 'confidence')])
        else:
            avg_confidence = 0.5
            trend_consistency = 0.5
        
        # Overall confidence
        confidence = (data_quality * 0.4 + avg_confidence * 0.4 + trend_consistency * 0.2)
        state['confidence_score'] = min(1.0, max(0.0, confidence))
        
        return state
    
    def _calculate_trend_slope(self, values: np.ndarray) -> float:
        """Calculate trend slope using linear regression"""
        if len(values) < 2:
            return 0.0
        
        x = np.arange(len(values))
        slope = np.polyfit(x, values, 1)[0]
        return slope


def create_langgraph_trend_analysis(repository_data: Dict, commit_history: List[Dict]) -> Dict:
    """Create LangGraph-based trend analysis"""
    analyzer = LangGraphTrendAnalyzer()
    return analyzer.analyze_trends(repository_data, commit_history)
