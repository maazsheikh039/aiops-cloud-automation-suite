import json
import subprocess
from typing import List, Dict

class TestSuggester:
    """Generates test suggestions using AI based on code analysis."""
    
    def __init__(self, model_name: str = "codellama:7b"):
        self.model_name = model_name
    
    def generate_prompt(self, function_data: Dict) -> str:
        """Create structured prompt for AI model."""
        prompt = f"""
You are an expert QA and Python testing engineer. Analyze the following function and suggest comprehensive unit test cases (using pytest format).

Function Name: {function_data.get('name')}
Parameters: {function_data.get('params')}
Docstring: {function_data.get('docstring')}
Complexity Metrics: {function_data.get('complexity')}

Provide test recommendations covering:
1. Happy path cases
2. Edge cases and boundary conditions
3. Error handling / exception testing

Format your output clearly with test descriptions and suggested assertions.
"""
        return prompt.strip()
    
    def call_ollama(self, prompt: str) -> str:
        """Call Ollama CLI to generate test suggestions."""
        try:
            cmd = ["ollama", "run", self.model_name, prompt]
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
            if result.returncode == 0:
                return result.stdout.strip()
            else:
                return f"Error running Ollama: {result.stderr.strip()}"
        except Exception as e:
            return f"Exception during Ollama call: {str(e)}"
    
    def suggest_tests(self, function_data: Dict) -> Dict:
        """Generate complete test suggestions for a function."""
        prompt = self.generate_prompt(function_data)
        ai_response = self.call_ollama(prompt)
        
        return {
            "function_name": function_data.get('name'),
            "suggestions": ai_response
        }
