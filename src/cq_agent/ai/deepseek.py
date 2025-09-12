"""
DeepSeek AI Integration for Code Quality Analysis
Provides Q&A and intelligent severity scoring using DeepSeek API
"""

import requests
import time
import os
from collections import deque
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from random import uniform


@dataclass
class DeepSeekResponse:
    """Response from DeepSeek API"""
    success: bool
    content: str
    error: Optional[str] = None


class DeepSeekClient:
    """Client for DeepSeek API integration"""
    
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://api.deepseek.com/v1"
        self.headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        # Rate limit configuration (defaults; overridable via env)
        self.max_per_minute: int = int(os.getenv("DEEPSEEK_RATE_LIMIT_PER_MIN", "60"))
        self._request_times: deque[float] = deque(maxlen=self.max_per_minute)
        self._min_interval: float = 60.0 / max(1, self.max_per_minute)
    
    def _respect_rate_limit(self) -> None:
        """Simple sliding-window rate limiter: max_per_minute requests."""
        now = time.time()
        # Drop timestamps older than 60s
        while self._request_times and now - self._request_times[0] > 60.0:
            self._request_times.popleft()
        if len(self._request_times) >= self.max_per_minute:
            # Wait until oldest falls out of the 60s window
            wait_s = 60.0 - (now - self._request_times[0]) + uniform(0.05, 0.15)
            time.sleep(max(0.0, wait_s))
        else:
            # Enforce minimal spacing between requests to smooth bursts
            if self._request_times:
                since_last = now - self._request_times[-1]
                if since_last < self._min_interval:
                    time.sleep(self._min_interval - since_last + uniform(0.01, 0.03))

    def _make_request(self, messages: List[Dict[str, str]], model: str = "deepseek-chat") -> DeepSeekResponse:
        """Make a request to DeepSeek API"""
        try:
            payload = {
                "model": model,
                "messages": messages,
                "temperature": 0.3,
                "max_tokens": 2000,
                "stream": False
            }

            # Retry with exponential backoff for transient errors and 429
            max_retries = 3
            backoff = 1.0
            for attempt in range(max_retries + 1):
                self._respect_rate_limit()
                response = requests.post(
                    f"{self.base_url}/chat/completions",
                    headers=self.headers,
                    json=payload,
                    timeout=30
                )
                # Record timestamp for rate limiting window
                self._request_times.append(time.time())

                if response.status_code == 200:
                    data = response.json()
                    content = data["choices"][0]["message"]["content"]
                    return DeepSeekResponse(success=True, content=content)

                # Handle specific errors
                if response.status_code in (429, 500, 502, 503, 504):
                    # Honor Retry-After if present
                    retry_after = response.headers.get("Retry-After")
                    if retry_after:
                        try:
                            time.sleep(float(retry_after))
                        except Exception:
                            time.sleep(backoff)
                    else:
                        time.sleep(backoff)
                    backoff *= 2
                    continue

                # Non-retryable errors (e.g., 401, 402, 400)
                error_msg = f"API Error {response.status_code}: {response.text}"
                return DeepSeekResponse(success=False, content="", error=error_msg)

            # If all retries exhausted
            return DeepSeekResponse(success=False, content="", error="Rate limit or transient error after retries")

        except Exception as e:
            return DeepSeekResponse(success=False, content="", error=str(e))
    
    def analyze_code_quality(self, code: str, file_path: str, language: str) -> DeepSeekResponse:
        """Analyze code quality and provide insights"""
        messages = [
            {
                "role": "system",
                "content": """You are an expert code quality analyst. Analyze the provided code and identify:
1. Security vulnerabilities
2. Performance issues
3. Code complexity problems
4. Best practice violations
5. Potential bugs

Provide specific, actionable recommendations. Focus on critical issues first."""
            },
            {
                "role": "user",
                "content": f"""Analyze this {language} code from {file_path}:

```{language}
{code}
```

Provide a detailed quality analysis with specific issues and recommendations."""
            }
        ]
        
        return self._make_request(messages)
    
    def score_severity(self, issue_title: str, issue_description: str, file_path: str, code_context: str = "") -> DeepSeekResponse:
        """Score the severity of a code quality issue"""
        messages = [
            {
                "role": "system",
                "content": """You are a code quality expert. Score the severity of issues on a scale of 1-10:
- 1-3: Low (cosmetic, style issues)
- 4-6: Medium (potential problems, maintainability)
- 7-8: High (bugs, security concerns)
- 9-10: Critical (severe security, data loss, system failure)

Consider impact, likelihood, and fix complexity. Respond with only the number and brief justification."""
            },
            {
                "role": "user",
                "content": f"""Score the severity of this issue:

Title: {issue_title}
Description: {issue_description}
File: {file_path}
Context: {code_context[:500] if code_context else "No context available"}

Provide severity score (1-10) and brief justification."""
            }
        ]
        
        return self._make_request(messages)
    
    def answer_question(self, question: str, codebase_context: str, relevant_files: List[str]) -> DeepSeekResponse:
        """Answer questions about the codebase"""
        context_info = "\n".join([f"- {file}" for file in relevant_files[:10]])  # Limit to 10 files
        
        messages = [
            {
                "role": "system",
                "content": """You are a helpful code assistant. Answer questions about the codebase based on the provided context. 
Be specific, accurate, and provide code examples when relevant. If you don't have enough information, say so."""
            },
            {
                "role": "user",
                "content": f"""Question: {question}

Codebase Context:
{codebase_context}

Relevant Files:
{context_info}

Please provide a detailed answer with specific examples from the codebase."""
            }
        ]
        
        return self._make_request(messages)
    
    def suggest_fixes(self, issue_title: str, issue_description: str, code_snippet: str, language: str) -> DeepSeekResponse:
        """Suggest specific fixes for code issues"""
        messages = [
            {
                "role": "system",
                "content": f"""You are an expert {language} developer. Provide specific, actionable fixes for code issues.
Include:
1. The exact code changes needed
2. Before/after examples
3. Explanation of why the fix works
4. Alternative approaches if applicable

Be practical and focus on implementable solutions."""
            },
            {
                "role": "user",
                "content": f"""Issue: {issue_title}
Description: {issue_description}

Code to fix:
```{language}
{code_snippet}
```

Provide specific fixes with code examples."""
            }
        ]
        
        return self._make_request(messages)


def enhance_issues_with_ai(issues: List[Dict], repo_data: Dict, api_key: str) -> List[Dict]:
    """Enhance issues with AI-powered severity scoring and suggestions"""
    if not api_key:
        return issues
    
    client = DeepSeekClient(api_key)
    enhanced_issues = []
    # Limit number of AI calls per run to avoid exhausting quota (configurable)
    max_ai_issues = int(os.getenv("DEEPSEEK_MAX_ISSUES_PER_RUN", "50"))
    to_process = issues[:max_ai_issues] if max_ai_issues > 0 else issues
    
    for issue in to_process:
        enhanced_issue = issue.copy()
        
        # Get code context for the issue
        file_path = issue.get("file", "")
        code_context = ""
        if file_path in repo_data.get("files", {}):
            file_data = repo_data["files"][file_path]
            if hasattr(file_data, 'text'):
                code_context = file_data.text
            else:
                code_context = file_data.get("text", "")
        
        # Get AI severity score
        severity_response = client.score_severity(
            issue.get("title", ""),
            issue.get("description", ""),
            file_path,
            code_context
        )
        
        if severity_response.success:
            try:
                # Extract severity score from response
                content = severity_response.content.strip()
                lines = content.split('\n')
                score_line = lines[0] if lines else content
                
                # Extract number from response
                import re
                score_match = re.search(r'(\d+)', score_line)
                if score_match:
                    ai_score = int(score_match.group(1))
                    # Map to our severity levels
                    if ai_score >= 9:
                        enhanced_issue["ai_severity"] = "critical"
                    elif ai_score >= 7:
                        enhanced_issue["ai_severity"] = "high"
                    elif ai_score >= 4:
                        enhanced_issue["ai_severity"] = "medium"
                    else:
                        enhanced_issue["ai_severity"] = "low"
                    
                    enhanced_issue["ai_justification"] = content
                else:
                    enhanced_issue["ai_severity"] = issue.get("severity", "medium")
                    enhanced_issue["ai_justification"] = "AI analysis failed to extract score"
            except:
                enhanced_issue["ai_severity"] = issue.get("severity", "medium")
                enhanced_issue["ai_justification"] = "AI analysis error"
        else:
            enhanced_issue["ai_severity"] = issue.get("severity", "medium")
            enhanced_issue["ai_justification"] = f"AI analysis failed: {severity_response.error}"
        
        # Get AI suggestions for fixes
        if code_context:
            fix_response = client.suggest_fixes(
                issue.get("title", ""),
                issue.get("description", ""),
                code_context[:1000],  # Limit context size
                issue.get("language", "python")
            )
            
            if fix_response.success:
                enhanced_issue["ai_suggestions"] = fix_response.content
            else:
                enhanced_issue["ai_suggestions"] = f"AI suggestions failed: {fix_response.error}"
        
        enhanced_issues.append(enhanced_issue)
    
    # Append any remaining issues unchanged if we limited processing
    if len(to_process) < len(issues):
        enhanced_issues.extend(issues[len(to_process):])

    return enhanced_issues


def answer_codebase_question(question: str, repo_data: Dict, api_key: str) -> str:
    """Answer a question about the codebase using AI"""
    if not api_key:
        return "DeepSeek API key not provided. Please configure it in the sidebar."
    
    client = DeepSeekClient(api_key)
    
    # Prepare codebase context
    files_info = []
    for file_path, file_data in repo_data.get("files", {}).items():
        if hasattr(file_data, 'language'):
            language = file_data.language
            sloc = file_data.sloc
        else:
            language = file_data.get("language", "unknown")
            sloc = file_data.get("sloc", 0)
        
        files_info.append(f"{file_path} ({language}, {sloc} lines)")
    
    context = f"Repository with {len(files_info)} files:\n" + "\n".join(files_info[:20])  # Limit context
    
    response = client.answer_question(question, context, list(repo_data.get("files", {}).keys())[:10])
    
    if response.success:
        return response.content
    else:
        return f"Error getting AI response: {response.error}"
