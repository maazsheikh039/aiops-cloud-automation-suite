import json
import os
import argparse
from code_analyzer import CodeAnalyzer
from test_suggester import TestSuggester

class TestSuggestionPipeline:
    """Orchestrates the complete test suggestion workflow."""
    
    def __init__(self, repo_path: str, output_dir: str = "./test_suggestions"):
        self.analyzer = CodeAnalyzer(repo_path)
        self.suggester = TestSuggester()
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)
    
    def run(self, commit_range: str = "HEAD~1..HEAD") -> Dict:
        """Execute the complete pipeline."""
        changed_files = self.analyzer.get_changed_files(commit_range)
        all_suggestions = []
        total_functions = 0
        
        for file_path in changed_files:
            functions = self.analyzer.extract_functions(file_path)
            for func in functions:
                total_functions += 1
                suggestion = self.suggester.suggest_tests(func)
                all_suggestions.append(suggestion)
                
        results = {
            "files_analyzed": changed_files,
            "functions_analyzed": total_functions,
            "suggestions": all_suggestions
        }
        
        # Save JSON output
        json_path = os.path.join(self.output_dir, "test_suggestions.json")
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2)
            
        # Generate and save report
        report_content = self.generate_report(results)
        report_path = os.path.join(self.output_dir, "report.md")
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write(report_content)
            
        print(f"Pipeline executed successfully. Reports saved to {self.output_dir}/")
        return results
    
    def generate_report(self, suggestions: Dict) -> str:
        """Generate human-readable markdown report."""
        report = "# AI Test Suggestion Pipeline Report\n\n"
        report += f"**Files Analyzed:** {len(suggestions['files_analyzed'])} files\n"
        report += f"**Functions Analyzed:** {suggestions['functions_analyzed']} functions\n\n"
        report += "---\n\n## Test Recommendations\n\n"
        
        for item in suggestions['suggestions']:
            report += f"### Function: `{item['function_name']}`\n\n"
            report += f"{item['suggestions']}\n\n"
            report += "---\n\n"
            
        return report

def main():
    parser = argparse.ArgumentParser(description="AI Test Suggestion Pipeline")
    parser.add_argument("--repo", default="./sample_project", help="Path to repository")
    parser.add_argument("--output", default="./test_suggestions", help="Output directory")
    parser.add_argument("--commit-range", default="HEAD~1..HEAD", help="Git commit range")
    
    args = parser.parse_args()
    
    pipeline = TestSuggestionPipeline(repo_path=args.repo, output_dir=args.output)
    pipeline.run(commit_range=args.commit_range)

if __name__ == "__main__":
    main()
