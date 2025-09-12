"""
GitHub API Integration
Provides GitHub API integration for PR comments and repository analysis
"""

import os
import requests
import json
from pathlib import Path


class GitHubIntegration:
    """GitHub API integration for code quality analysis"""
    
    def __init__(self, token: Optional[str] = None):
        self.token = token or os.getenv('GITHUB_TOKEN')
        self.base_url = "https://api.github.com"
        self.headers = {
            'Authorization': f'token {self.token}' if self.token else None,
            'Accept': 'application/vnd.github.v3+json',
            'User-Agent': 'Code-Quality-Agent/1.0'
        }
        
    def is_authenticated(self) -> bool:
        """Check if GitHub API is authenticated"""
        if not self.token:
            return False
        
        try:
            response = requests.get(f"{self.base_url}/user", headers=self.headers)
            return response.status_code == 200
        except:
            return False
    
    def get_repository_info(self, owner: str, repo: str) -> Optional[Dict]:
        """Get repository information"""
        try:
            response = requests.get(
                f"{self.base_url}/repos/{owner}/{repo}",
                headers=self.headers
            )
            if response.status_code == 200:
                return response.json()
        except:
            pass
        return None
    
    def get_pull_requests(self, owner: str, repo: str, state: str = 'open') -> List[Dict]:
        """Get pull requests for a repository"""
        try:
            response = requests.get(
                f"{self.base_url}/repos/{owner}/{repo}/pulls",
                headers=self.headers,
                params={'state': state, 'per_page': 100}
            )
            if response.status_code == 200:
                return response.json()
        except:
            pass
        return []
    
    def get_pull_request_files(self, owner: str, repo: str, pr_number: int) -> List[Dict]:
        """Get files changed in a pull request"""
        try:
            response = requests.get(
                f"{self.base_url}/repos/{owner}/{repo}/pulls/{pr_number}/files",
                headers=self.headers
            )
            if response.status_code == 200:
                return response.json()
        except:
            pass
        return []
    
    def create_pull_request_comment(self, owner: str, repo: str, pr_number: int, 
                                  body: str, path: str, line: int) -> bool:
        """Create a comment on a pull request"""
        if not self.is_authenticated():
            return False
        
        try:
            data = {
                'body': body,
                'path': path,
                'line': line,
                'side': 'RIGHT'
            }
            
            response = requests.post(
                f"{self.base_url}/repos/{owner}/{repo}/pulls/{pr_number}/comments",
                headers=self.headers,
                json=data
            )
            return response.status_code == 201
        except:
            return False
    
    def create_issue_comment(self, owner: str, repo: str, issue_number: int, body: str) -> bool:
        """Create a comment on an issue"""
        if not self.is_authenticated():
            return False
        
        try:
            data = {'body': body}
            
            response = requests.post(
                f"{self.base_url}/repos/{owner}/{repo}/issues/{issue_number}/comments",
                headers=self.headers,
                json=data
            )
            return response.status_code == 201
        except:
            return False
    
    def create_issue(self, owner: str, repo: str, title: str, body: str, 
                    labels: List[str] = None) -> Optional[Dict]:
        """Create a new issue"""
        if not self.is_authenticated():
            return None
        
        try:
            data = {
                'title': title,
                'body': body,
                'labels': labels or []
            }
            
            response = requests.post(
                f"{self.base_url}/repos/{owner}/{repo}/issues",
                headers=self.headers,
                json=data
            )
            if response.status_code == 201:
                return response.json()
        except:
            pass
        return None
    
    def get_workflow_runs(self, owner: str, repo: str) -> List[Dict]:
        """Get recent workflow runs"""
        try:
            response = requests.get(
                f"{self.base_url}/repos/{owner}/{repo}/actions/runs",
                headers=self.headers,
                params={'per_page': 10}
            )
            if response.status_code == 200:
                return response.json().get('workflow_runs', [])
        except:
            pass
        return []
    
    def create_check_run(self, owner: str, repo: str, sha: str, name: str, 
                        status: str, conclusion: str, output: Dict) -> bool:
        """Create a check run for a commit"""
        if not self.is_authenticated():
            return False
        
        try:
            data = {
                'name': name,
                'head_sha': sha,
                'status': status,  # 'completed', 'in_progress', 'queued'
                'conclusion': conclusion,  # 'success', 'failure', 'neutral', 'cancelled', 'timed_out', 'action_required'
                'output': output
            }
            
            response = requests.post(
                f"{self.base_url}/repos/{owner}/{repo}/check-runs",
                headers=self.headers,
                json=data
            )
            return response.status_code == 201
        except:
            return False


class CodeQualityGitHubBot:
    """GitHub bot for automated code quality analysis"""
    
    def __init__(self, github_integration: GitHubIntegration):
        self.github = github_integration
    
    def analyze_pull_request(self, owner: str, repo: str, pr_number: int, 
                           issues: List[Dict]) -> Dict:
        """Analyze a pull request and create appropriate comments"""
        if not self.github.is_authenticated():
            return {'error': 'GitHub authentication required'}
        
        # Get PR files
        pr_files = self.github.get_pull_request_files(owner, repo, pr_number)
        
        # Group issues by file
        file_issues = {}
        for issue in issues:
            file_path = issue.get('file', '')
            if file_path not in file_issues:
                file_issues[file_path] = []
            file_issues[file_path].append(issue)
        
        # Create comments for each file with issues
        comments_created = 0
        for pr_file in pr_files:
            file_path = pr_file.get('filename', '')
            if file_path in file_issues:
                file_issues_list = file_issues[file_path]
                
                # Create summary comment
                summary_comment = self._create_summary_comment(file_issues_list)
                
                # Post comment
                if self.github.create_pull_request_comment(
                    owner, repo, pr_number, summary_comment, file_path, 1
                ):
                    comments_created += 1
        
        return {
            'comments_created': comments_created,
            'files_analyzed': len(file_issues),
            'total_issues': len(issues)
        }
    
    def _create_summary_comment(self, issues: List[Dict]) -> str:
        """Create a summary comment for issues in a file"""
        if not issues:
            return ""
        
        # Group by severity
        severity_groups = {'critical': [], 'high': [], 'medium': [], 'low': []}
        for issue in issues:
            severity = issue.get('severity', 'low')
            if severity in severity_groups:
                severity_groups[severity].append(issue)
        
        comment = "## 🔍 Code Quality Analysis\n\n"
        
        # Summary
        total_issues = len(issues)
        comment += f"Found **{total_issues}** code quality issues in this file:\n\n"
        
        # Severity breakdown
        for severity, issues_list in severity_groups.items():
            if issues_list:
                emoji = {'critical': '🔴', 'high': '🟠', 'medium': '🟡', 'low': '🟢'}[severity]
                comment += f"- {emoji} **{severity.title()}**: {len(issues_list)} issues\n"
        
        comment += "\n### 📋 Issues Found:\n\n"
        
        # List issues
        for i, issue in enumerate(issues[:10], 1):  # Limit to 10 issues
            severity = issue.get('severity', 'low')
            emoji = {'critical': '🔴', 'high': '🟠', 'medium': '🟡', 'low': '🟢'}[severity]
            
            comment += f"**{i}. {emoji} {issue.get('title', 'Issue')}**\n"
            comment += f"- **Severity**: {severity.title()}\n"
            comment += f"- **Line**: {issue.get('line', 'N/A')}\n"
            comment += f"- **Description**: {issue.get('message', 'No description')}\n"
            
            if issue.get('fix'):
                comment += f"- **Suggested Fix**: `{issue['fix']}`\n"
            
            comment += "\n"
        
        if len(issues) > 10:
            comment += f"\n*... and {len(issues) - 10} more issues. Use the full report for complete analysis.*\n"
        
        comment += "\n---\n*🤖 Automated by Code Quality Intelligence Agent*"
        
        return comment
    
    def create_quality_report_issue(self, owner: str, repo: str, 
                                  repo_summary: Dict, issues: List[Dict]) -> Optional[Dict]:
        """Create a GitHub issue with quality report"""
        if not self.github.is_authenticated():
            return None
        
        # Calculate quality score
        total_issues = len(issues)
        critical_issues = len([i for i in issues if i.get('severity') == 'critical'])
        high_issues = len([i for i in issues if i.get('severity') == 'high'])
        
        # Create issue title and body
        title = f"📊 Code Quality Report - {total_issues} issues found"
        
        body = f"""## 📊 Code Quality Analysis Report

### 📈 Summary
- **Total Issues**: {total_issues}
- **Critical Issues**: {critical_issues} 🔴
- **High Priority Issues**: {high_issues} 🟠
- **Files Analyzed**: {repo_summary.get('total_files', 0)}
- **Lines of Code**: {repo_summary.get('total_sloc', 0)}

### 🎯 Quality Score
"""
        
        # Add quality score visualization
        if total_issues == 0:
            body += "🟢 **Excellent!** No issues found.\n\n"
        elif critical_issues > 0:
            body += "🔴 **Critical Issues Detected** - Immediate attention required.\n\n"
        elif high_issues > 5:
            body += "🟠 **High Priority Issues** - Should be addressed soon.\n\n"
        else:
            body += "🟡 **Moderate Issues** - Consider addressing in next iteration.\n\n"
        
        # Add top issues
        if issues:
            body += "### 🔥 Top Issues\n\n"
            for i, issue in enumerate(issues[:5], 1):
                severity = issue.get('severity', 'low')
                emoji = {'critical': '🔴', 'high': '🟠', 'medium': '🟡', 'low': '🟢'}[severity]
                body += f"{i}. {emoji} **{issue.get('title', 'Issue')}** in `{issue.get('file', 'unknown')}`\n"
        
        body += "\n### 🛠️ Next Steps\n"
        body += "1. Review the detailed analysis in the attached report\n"
        body += "2. Prioritize critical and high-severity issues\n"
        body += "3. Use the suggested fixes where applicable\n"
        body += "4. Consider implementing automated quality checks\n\n"
        body += "---\n*🤖 Generated by Code Quality Intelligence Agent*"
        
        # Create issue
        labels = ['code-quality', 'analysis']
        if critical_issues > 0:
            labels.append('critical')
        elif high_issues > 5:
            labels.append('high-priority')
        
        return self.github.create_issue(owner, repo, title, body, labels)


def create_github_integration(token: Optional[str] = None) -> GitHubIntegration:
    """Create GitHub integration instance"""
    return GitHubIntegration(token)


def create_github_bot(token: Optional[str] = None) -> CodeQualityGitHubBot:
    """Create GitHub bot instance"""
    github = GitHubIntegration(token)
    return CodeQualityGitHubBot(github)
