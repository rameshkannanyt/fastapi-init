from pathlib import Path
from typing import Dict, List

def analyze_async_patterns(code: str) -> List[str]:
    """Analyze the provided code for potential async/sync pitfalls."""
    issues = []
    
    # Check for blocking calls in async functions
    if "time.sleep" in code:
        issues.append("Blocking call 'time.sleep' found in async function. Consider using 'await asyncio.sleep' instead.")
    
    # Check for synchronous functions in async context
    if "def " in code and "async def" not in code:
        issues.append("Synchronous function defined in async context. Ensure proper usage of async functions.")
    
    # Additional checks can be added here
    
    return issues


def analyze_file(file_path: Path) -> List[str]:
    """Analyze a Python file for async/sync issues."""
    issues = []
    
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            code = f.read()
            issues.extend(analyze_async_patterns(code))
    except Exception as e:
        issues.append(f"Error reading file {file_path}: {e}")
    
    return issues


def analyze_project(project_path: Path) -> Dict[Path, List[str]]:
    """Analyze the entire project for async/sync issues."""
    issues_by_file = {}
    
    for file_path in project_path.rglob("*.py"):
        issues = analyze_file(file_path)
        if issues:
            issues_by_file[file_path] = issues
    
    return issues_by_file


class AsyncAnalyzer:
    """Analyzes FastAPI projects for async/sync issues and best practices."""
    
    def __init__(self):
        pass
    
    def analyze(self, project_path: Path) -> Dict[Path, List[str]]:
        """Analyze the project for async/sync issues."""
        return analyze_project(project_path)
    
    def get_analysis_summary(self, project_path: Path) -> str:
        """Get a summary of the async analysis."""
        issues_by_file = self.analyze(project_path)
        
        if not issues_by_file:
            return "No async/sync issues found in the project."
        
        summary_lines = ["Async/Sync Analysis Summary:"]
        for file_path, issues in issues_by_file.items():
            summary_lines.append(f"\n{file_path}:")
            for issue in issues:
                summary_lines.append(f"  - {issue}")
        
        return "\n".join(summary_lines)