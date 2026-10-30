import ast
import os
from typing import List, Dict
from git import Repo

class CodeAnalyzer:
    """Analyzes code changes and extracts relevant information for test suggestions."""
    
    def __init__(self, repo_path: str):
        """
        Initialize the code analyzer.
        """
        self.repo_path = repo_path
        try:
            self.repo = Repo(repo_path)
        except Exception:
            self.repo = None
    
    def get_changed_files(self, commit_range: str = "HEAD~1..HEAD") -> List[str]:
        """
        Get list of changed Python files in the commit range.
        """
        changed_files = []
        if not self.repo:
            # Fallback for sample directory if git log isn't fully staged
            for root, dirs, files in os.walk(self.repo_path):
                for file in files:
                    if file.endswith('.py'):
                        changed_files.append(os.path.join(root, file))
            return changed_files
            
        try:
            diffs = self.repo.head.commit.diff(self.repo.commit("HEAD~1"))
            for diff_item in diffs:
                if diff_item.a_path.endswith('.py'):
                    changed_files.append(os.path.join(self.repo_path, diff_item.a_path))
        except Exception:
            # Fallback to scanning all .py files in repo if commit range is single commit / fresh repo
            for root, dirs, files in os.walk(self.repo_path):
                for file in files:
                    if file.endswith('.py'):
                        changed_files.append(os.path.join(root, file))
        return list(set(changed_files))
    
    def analyze_complexity(self, function_node: ast.FunctionDef) -> Dict:
        """
        Analyze function complexity metrics (branches and loops).
        """
        branches = 0
        loops = 0
        for node in ast.walk(function_node):
            if isinstance(node, (ast.If, ast.IfExp, ast.Try, ast.ExceptHandler)):
                branches += 1
            elif isinstance(node, (ast.For, ast.While, ast.AsyncFor)):
                loops += 1
        
        # Cyclomatic complexity approximation: E - N + 2P -> branches + 1
        cyclomatic = branches + 1
        return {
            "branches": branches,
            "loops": loops,
            "cyclomatic_complexity": cyclomatic
        }

    def extract_functions(self, file_path: str) -> List[Dict]:
        """
        Extract function definitions and metadata from a Python file.
        """
        functions = []
        if not os.path.exists(file_path):
            return functions
            
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        try:
            tree = ast.parse(content)
        except SyntaxError:
            return functions
            
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                params = [arg.arg for arg in node.args.args]
                docstring = ast.get_docstring(node) or "No docstring provided."
                complexity = self.analyze_complexity(node)
                
                functions.append({
                    "name": node.name,
                    "params": params,
                    "docstring": docstring,
                    "complexity": complexity,
                    "lineno": node.lineno
                })
                
        return functions
