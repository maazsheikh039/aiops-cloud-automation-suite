import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from code_analyzer import CodeAnalyzer

def test_analyzer():
    analyzer = CodeAnalyzer('sample_project')
    calc_path = os.path.join('sample_project', 'calculator.py')
    
    # Test function extraction
    functions = analyzer.extract_functions(calc_path)
    print(f"Found {len(functions)} functions")
    
    for func in functions:
        print(f"Function: {func['name']}")
        print(f"Parameters: {func['params']}")
        print(f"Complexity: {func['complexity']}")
        print("---")

if __name__ == "__main__":
    test_analyzer()
