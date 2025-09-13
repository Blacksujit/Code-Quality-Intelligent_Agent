"""
Agentic Patterns with Multi-step Reasoning
Implements intelligent reasoning workflows for code quality analysis
"""

from dataclasses import dataclass
from enum import Enum
import re
from pathlib import Path
from typing import Dict, List, Tuple, Optional, Any


class ReasoningStep(Enum):
    """Types of reasoning steps"""
    ANALYZE = "analyze"
    IDENTIFY = "identify"
    PRIORITIZE = "prioritize"
    SUGGEST = "suggest"
    VALIDATE = "validate"
    REFINE = "refine"


@dataclass
class ReasoningContext:
    """Context for reasoning process"""
    repository_path: str
    file_path: str
    code_content: str
    language: str
    issues: List[Dict]
    metrics: Dict
    previous_steps: List[Dict]
    current_goal: str


@dataclass
class ReasoningResult:
    """Result of a reasoning step"""
    step_type: ReasoningStep
    confidence: float
    reasoning: str
    suggestions: List[str]
    next_steps: List[str]
    evidence: List[Dict]


class CodeQualityReasoner:
    """Multi-step reasoning engine for code quality analysis"""
    
    def __init__(self):
        self.reasoning_patterns = {
            'security_analysis': self._security_reasoning_pattern,
            'performance_optimization': self._performance_reasoning_pattern,
            'maintainability_improvement': self._maintainability_reasoning_pattern,
            'architecture_review': self._architecture_reasoning_pattern,
            'testing_strategy': self._testing_reasoning_pattern
        }
    
    def reason_about_code(self, context: ReasoningContext) -> List[ReasoningResult]:
        """Main reasoning workflow"""
        results = []
        
        # Step 1: Analyze current state
        analysis_result = self._analyze_current_state(context)
        results.append(analysis_result)
        
        # Step 2: Identify patterns and issues
        identification_result = self._identify_patterns_and_issues(context, analysis_result)
        results.append(identification_result)
        
        # Step 3: Prioritize based on impact
        prioritization_result = self._prioritize_issues(context, identification_result)
        results.append(prioritization_result)
        
        # Step 4: Suggest improvements
        suggestion_result = self._suggest_improvements(context, prioritization_result)
        results.append(suggestion_result)
        
        # Step 5: Validate suggestions
        validation_result = self._validate_suggestions(context, suggestion_result)
        results.append(validation_result)
        
        # Step 6: Refine recommendations
        refinement_result = self._refine_recommendations(context, validation_result)
        results.append(refinement_result)
        
        return results
    
    def _analyze_current_state(self, context: ReasoningContext) -> ReasoningResult:
        """Analyze the current state of the code"""
        reasoning = f"Analyzing {context.file_path} ({context.language})...\n"
        
        # Analyze code metrics
        sloc = context.metrics.get('sloc', 0)
        complexity = context.metrics.get('complexity', 0)
        issues_count = len(context.issues)
        
        reasoning += f"- Lines of code: {sloc}\n"
        reasoning += f"- Cyclomatic complexity: {complexity}\n"
        reasoning += f"- Issues found: {issues_count}\n"
        
        # Analyze code structure
        if context.language == 'python':
            reasoning += self._analyze_python_structure(context)
        elif context.language in ['javascript', 'typescript']:
            reasoning += self._analyze_js_structure(context)
        
        # Determine overall health
        health_score = self._calculate_health_score(context)
        reasoning += f"- Overall health score: {health_score:.2f}/10\n"
        
        suggestions = []
        if health_score < 5:
            suggestions.append("Code needs significant improvement")
        elif health_score < 7:
            suggestions.append("Code has room for improvement")
        else:
            suggestions.append("Code is in good condition")
        
        next_steps = ["Identify specific patterns and issues", "Prioritize improvements"]
        
        return ReasoningResult(
            step_type=ReasoningStep.ANALYZE,
            confidence=0.9,
            reasoning=reasoning,
            suggestions=suggestions,
            next_steps=next_steps,
            evidence=[{'metric': 'health_score', 'value': health_score}]
        )
    
    def _identify_patterns_and_issues(self, context: ReasoningContext, analysis_result: ReasoningResult) -> ReasoningResult:
        """Identify patterns and issues in the code"""
        reasoning = "Identifying patterns and issues...\n"
        suggestions = []
        evidence = []
        
        # Security issues
        security_issues = [issue for issue in context.issues if issue.get('category') == 'security']
        if security_issues:
            reasoning += f"- Found {len(security_issues)} security issues\n"
            suggestions.append("Address security vulnerabilities immediately")
            evidence.append({'type': 'security_issues', 'count': len(security_issues)})
        
        # Performance issues
        performance_issues = [issue for issue in context.issues if issue.get('category') == 'performance']
        if performance_issues:
            reasoning += f"- Found {len(performance_issues)} performance issues\n"
            suggestions.append("Optimize performance bottlenecks")
            evidence.append({'type': 'performance_issues', 'count': len(performance_issues)})
        
        # Code quality issues
        quality_issues = [issue for issue in context.issues if issue.get('category') == 'quality']
        if quality_issues:
            reasoning += f"- Found {len(quality_issues)} code quality issues\n"
            suggestions.append("Improve code quality and maintainability")
            evidence.append({'type': 'quality_issues', 'count': len(quality_issues)})
        
        # Complexity issues
        complexity = context.metrics.get('complexity', 0)
        if complexity > 10:
            reasoning += f"- High complexity detected ({complexity})\n"
            suggestions.append("Reduce cyclomatic complexity")
            evidence.append({'type': 'high_complexity', 'value': complexity})
        
        # Duplication issues
        duplication_issues = [issue for issue in context.issues if 'duplicate' in issue.get('title', '').lower()]
        if duplication_issues:
            reasoning += f"- Found {len(duplication_issues)} duplication issues\n"
            suggestions.append("Eliminate code duplication")
            evidence.append({'type': 'duplication_issues', 'count': len(duplication_issues)})
        
        next_steps = ["Prioritize issues by impact", "Generate specific improvement suggestions"]
        
        return ReasoningResult(
            step_type=ReasoningStep.IDENTIFY,
            confidence=0.85,
            reasoning=reasoning,
            suggestions=suggestions,
            next_steps=next_steps,
            evidence=evidence
        )
    
    def _prioritize_issues(self, context: ReasoningContext, identification_result: ReasoningResult) -> ReasoningResult:
        """Prioritize issues based on impact and severity"""
        reasoning = "Prioritizing issues by impact and severity...\n"
        suggestions = []
        evidence = []
        
        # Group issues by severity
        critical_issues = [issue for issue in context.issues if issue.get('severity') == 'critical']
        high_issues = [issue for issue in context.issues if issue.get('severity') == 'high']
        medium_issues = [issue for issue in context.issues if issue.get('severity') == 'medium']
        low_issues = [issue for issue in context.issues if issue.get('severity') == 'low']
        
        reasoning += f"- Critical: {len(critical_issues)} issues\n"
        reasoning += f"- High: {len(high_issues)} issues\n"
        reasoning += f"- Medium: {len(medium_issues)} issues\n"
        reasoning += f"- Low: {len(low_issues)} issues\n"
        
        # Prioritization logic
        if critical_issues:
            reasoning += "🚨 CRITICAL: Address security and critical issues immediately\n"
            suggestions.append("Fix critical issues first - they pose immediate risks")
            evidence.append({'priority': 'critical', 'count': len(critical_issues)})
        
        if high_issues:
            reasoning += "⚠️ HIGH: Address high-priority issues in next sprint\n"
            suggestions.append("Plan high-priority fixes for next development cycle")
            evidence.append({'priority': 'high', 'count': len(high_issues)})
        
        if medium_issues:
            reasoning += "📋 MEDIUM: Address medium-priority issues when possible\n"
            suggestions.append("Include medium-priority fixes in regular maintenance")
            evidence.append({'priority': 'medium', 'count': len(medium_issues)})
        
        if low_issues:
            reasoning += "💡 LOW: Address low-priority issues during refactoring\n"
            suggestions.append("Address low-priority issues during code refactoring")
            evidence.append({'priority': 'low', 'count': len(low_issues)})
        
        next_steps = ["Generate specific improvement suggestions", "Create implementation plan"]
        
        return ReasoningResult(
            step_type=ReasoningStep.PRIORITIZE,
            confidence=0.9,
            reasoning=reasoning,
            suggestions=suggestions,
            next_steps=next_steps,
            evidence=evidence
        )
    
    def _suggest_improvements(self, context: ReasoningContext, prioritization_result: ReasoningResult) -> ReasoningResult:
        """Suggest specific improvements"""
        reasoning = "Generating improvement suggestions...\n"
        suggestions = []
        evidence = []
        
        # Security improvements
        security_issues = [issue for issue in context.issues if issue.get('category') == 'security']
        if security_issues:
            reasoning += "🔒 Security improvements:\n"
            for issue in security_issues[:3]:  # Top 3 security issues
                if issue.get('fix'):
                    reasoning += f"- {issue.get('title', 'Security issue')}: {issue['fix']}\n"
                    suggestions.append(f"Security fix: {issue['fix']}")
                    evidence.append({'type': 'security_fix', 'issue': issue['title']})
        
        # Performance improvements
        performance_issues = [issue for issue in context.issues if issue.get('category') == 'performance']
        if performance_issues:
            reasoning += "⚡ Performance improvements:\n"
            for issue in performance_issues[:3]:  # Top 3 performance issues
                if issue.get('fix'):
                    reasoning += f"- {issue.get('title', 'Performance issue')}: {issue['fix']}\n"
                    suggestions.append(f"Performance fix: {issue['fix']}")
                    evidence.append({'type': 'performance_fix', 'issue': issue['title']})
        
        # Code quality improvements
        quality_issues = [issue for issue in context.issues if issue.get('category') == 'quality']
        if quality_issues:
            reasoning += "📝 Code quality improvements:\n"
            for issue in quality_issues[:3]:  # Top 3 quality issues
                if issue.get('fix'):
                    reasoning += f"- {issue.get('title', 'Quality issue')}: {issue['fix']}\n"
                    suggestions.append(f"Quality fix: {issue['fix']}")
                    evidence.append({'type': 'quality_fix', 'issue': issue['title']})
        
        # General improvements based on metrics
        complexity = context.metrics.get('complexity', 0)
        if complexity > 10:
            reasoning += f"🔧 Complexity reduction: Break down complex functions (current: {complexity})\n"
            suggestions.append("Refactor complex functions into smaller, focused functions")
            evidence.append({'type': 'complexity_reduction', 'current': complexity})
        
        sloc = context.metrics.get('sloc', 0)
        if sloc > 500:
            reasoning += f"📏 File size reduction: Consider splitting large file ({sloc} lines)\n"
            suggestions.append("Split large file into smaller, focused modules")
            evidence.append({'type': 'file_split', 'current_sloc': sloc})
        
        next_steps = ["Validate suggestions for feasibility", "Create implementation timeline"]
        
        return ReasoningResult(
            step_type=ReasoningStep.SUGGEST,
            confidence=0.8,
            reasoning=reasoning,
            suggestions=suggestions,
            next_steps=next_steps,
            evidence=evidence
        )
    
    def _validate_suggestions(self, context: ReasoningContext, suggestion_result: ReasoningResult) -> ReasoningResult:
        """Validate suggestions for feasibility and impact"""
        reasoning = "Validating suggestions for feasibility and impact...\n"
        suggestions = []
        evidence = []
        
        # Validate each suggestion
        for suggestion in suggestion_result.suggestions:
            validation = self._validate_single_suggestion(suggestion, context)
            reasoning += f"✓ {suggestion}: {validation['feasibility']} (Impact: {validation['impact']})\n"
            
            if validation['feasible']:
                suggestions.append(suggestion)
                evidence.append({
                    'suggestion': suggestion,
                    'feasible': True,
                    'impact': validation['impact'],
                    'effort': validation['effort']
                })
            else:
                reasoning += f"  ⚠️ Not feasible: {validation['reason']}\n"
        
        # Calculate overall validation score
        feasible_count = len([s for s in suggestion_result.suggestions if self._validate_single_suggestion(s, context)['feasible']])
        total_count = len(suggestion_result.suggestions)
        validation_score = feasible_count / total_count if total_count > 0 else 0
        
        reasoning += f"\nValidation score: {validation_score:.2f} ({feasible_count}/{total_count} suggestions feasible)\n"
        
        next_steps = ["Refine recommendations based on validation", "Create final implementation plan"]
        
        return ReasoningResult(
            step_type=ReasoningStep.VALIDATE,
            confidence=validation_score,
            reasoning=reasoning,
            suggestions=suggestions,
            next_steps=next_steps,
            evidence=evidence
        )
    
    def _refine_recommendations(self, context: ReasoningContext, validation_result: ReasoningResult) -> ReasoningResult:
        """Refine recommendations based on validation"""
        reasoning = "Refining recommendations for optimal implementation...\n"
        suggestions = []
        evidence = []
        
        # Group suggestions by effort and impact
        high_impact_low_effort = []
        high_impact_high_effort = []
        low_impact_low_effort = []
        low_impact_high_effort = []
        
        for item in validation_result.evidence:
            suggestion = item['suggestion']
            impact = item['impact']
            effort = item['effort']
            
            if impact == 'high' and effort == 'low':
                high_impact_low_effort.append(suggestion)
            elif impact == 'high' and effort == 'high':
                high_impact_high_effort.append(suggestion)
            elif impact == 'low' and effort == 'low':
                low_impact_low_effort.append(suggestion)
            else:
                low_impact_high_effort.append(suggestion)
        
        # Prioritize recommendations
        reasoning += "🎯 Prioritized recommendations:\n"
        
        if high_impact_low_effort:
            reasoning += "1. HIGH IMPACT, LOW EFFORT (Do first):\n"
            for suggestion in high_impact_low_effort:
                reasoning += f"   - {suggestion}\n"
                suggestions.append(suggestion)
                evidence.append({'priority': 1, 'impact': 'high', 'effort': 'low'})
        
        if high_impact_high_effort:
            reasoning += "2. HIGH IMPACT, HIGH EFFORT (Plan for next sprint):\n"
            for suggestion in high_impact_high_effort:
                reasoning += f"   - {suggestion}\n"
                suggestions.append(suggestion)
                evidence.append({'priority': 2, 'impact': 'high', 'effort': 'high'})
        
        if low_impact_low_effort:
            reasoning += "3. LOW IMPACT, LOW EFFORT (Do when convenient):\n"
            for suggestion in low_impact_low_effort:
                reasoning += f"   - {suggestion}\n"
                suggestions.append(suggestion)
                evidence.append({'priority': 3, 'impact': 'low', 'effort': 'low'})
        
        if low_impact_high_effort:
            reasoning += "4. LOW IMPACT, HIGH EFFORT (Consider carefully):\n"
            for suggestion in low_impact_high_effort:
                reasoning += f"   - {suggestion}\n"
                suggestions.append(suggestion)
                evidence.append({'priority': 4, 'impact': 'low', 'effort': 'high'})
        
        next_steps = ["Create implementation timeline", "Set up monitoring and tracking"]
        
        return ReasoningResult(
            step_type=ReasoningStep.REFINE,
            confidence=0.95,
            reasoning=reasoning,
            suggestions=suggestions,
            next_steps=next_steps,
            evidence=evidence
        )
    
    def _analyze_python_structure(self, context: ReasoningContext) -> str:
        """Analyze Python code structure"""
        analysis = ""
        
        # Look for common Python patterns
        if 'import' in context.code_content:
            analysis += "- Uses imports (good modularity)\n"
        
        if 'def ' in context.code_content:
            analysis += "- Contains functions (good structure)\n"
        
        if 'class ' in context.code_content:
            analysis += "- Uses classes (object-oriented design)\n"
        
        if 'try:' in context.code_content:
            analysis += "- Uses exception handling (good practice)\n"
        
        if 'async def' in context.code_content:
            analysis += "- Uses async/await (modern Python)\n"
        
        return analysis
    
    def _analyze_js_structure(self, context: ReasoningContext) -> str:
        """Analyze JavaScript/TypeScript code structure"""
        analysis = ""
        
        # Look for common JS patterns
        if 'import ' in context.code_content or 'require(' in context.code_content:
            analysis += "- Uses modules (good structure)\n"
        
        if 'function ' in context.code_content or '=>' in context.code_content:
            analysis += "- Contains functions (good structure)\n"
        
        if 'class ' in context.code_content:
            analysis += "- Uses classes (object-oriented design)\n"
        
        if 'try {' in context.code_content:
            analysis += "- Uses exception handling (good practice)\n"
        
        if 'async ' in context.code_content:
            analysis += "- Uses async/await (modern JavaScript)\n"
        
        return analysis
    
    def _calculate_health_score(self, context: ReasoningContext) -> float:
        """Calculate overall code health score (0-10)"""
        score = 10.0
        
        # Deduct for issues
        critical_issues = len([i for i in context.issues if i.get('severity') == 'critical'])
        high_issues = len([i for i in context.issues if i.get('severity') == 'high'])
        medium_issues = len([i for i in context.issues if i.get('severity') == 'medium'])
        low_issues = len([i for i in context.issues if i.get('severity') == 'low'])
        
        score -= critical_issues * 2.0  # Critical issues are very bad
        score -= high_issues * 1.0      # High issues are bad
        score -= medium_issues * 0.5    # Medium issues are somewhat bad
        score -= low_issues * 0.1       # Low issues are minor
        
        # Deduct for complexity
        complexity = context.metrics.get('complexity', 0)
        if complexity > 20:
            score -= 2.0
        elif complexity > 10:
            score -= 1.0
        elif complexity > 5:
            score -= 0.5
        
        # Deduct for file size
        sloc = context.metrics.get('sloc', 0)
        if sloc > 1000:
            score -= 1.0
        elif sloc > 500:
            score -= 0.5
        
        return max(0.0, min(10.0, score))
    
    def _validate_single_suggestion(self, suggestion: str, context: ReasoningContext) -> Dict:
        """Validate a single suggestion for feasibility"""
        # Simplified validation logic
        if 'security' in suggestion.lower():
            return {
                'feasible': True,
                'feasibility': 'High',
                'impact': 'high',
                'effort': 'medium',
                'reason': ''
            }
        elif 'performance' in suggestion.lower():
            return {
                'feasible': True,
                'feasibility': 'High',
                'impact': 'high',
                'effort': 'high',
                'reason': ''
            }
        elif 'complexity' in suggestion.lower():
            return {
                'feasible': True,
                'feasibility': 'Medium',
                'impact': 'medium',
                'effort': 'high',
                'reason': ''
            }
        else:
            return {
                'feasible': True,
                'feasibility': 'Medium',
                'impact': 'medium',
                'effort': 'medium',
                'reason': ''
            }


def create_reasoning_workflow(repository_path: str, file_path: str, 
                            code_content: str, language: str, 
                            issues: List[Dict], metrics: Dict) -> List[ReasoningResult]:
    """Create a reasoning workflow for code quality analysis"""
    context = ReasoningContext(
        repository_path=repository_path,
        file_path=file_path,
        code_content=code_content,
        language=language,
        issues=issues,
        metrics=metrics,
        previous_steps=[],
        current_goal="Improve code quality"
    )
    
    reasoner = CodeQualityReasoner()
    return reasoner.reason_about_code(context)
