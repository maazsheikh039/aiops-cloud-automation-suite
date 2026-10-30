#!/usr/bin/env python3
"""
CI Failure Triage Assistant
Analyzes CI logs and suggests likely causes of failures
"""

import sys
import yaml
import re
from pathlib import Path
from colorama import Fore, Style, init

# Initialize colorama for colored output
init(autoreset=True)

class CITriageAssistant:
    def __init__(self, patterns_file):
        """
        Initialize the triage assistant with failure patterns.
        
        Args:
            patterns_file: Path to YAML file containing failure patterns
        """
        self.patterns = self._load_patterns(patterns_file)
        self.log_content = ""
        self.matches = []
    
    def _load_patterns(self, patterns_file):
        """
        Load failure patterns from YAML file.
        """
        with open(patterns_file, 'r') as f:
            data = yaml.safe_load(f)
            return data.get('patterns', [])
    
    def analyze_log(self, log_file):
        """
        Analyze a CI log file for known failure patterns.
        """
        with open(log_file, 'r') as f:
            self.log_content = f.read().lower()
        
        self.matches = []
        
        for pattern in self.patterns:
            match_count = 0
            matched_keywords = []
            
            for keyword in pattern['keywords']:
                count = self.log_content.count(keyword.lower())
                if count > 0:
                    match_count += count
                    matched_keywords.append(keyword)
            
            if match_count > 0:
                self.matches.append({
                    'pattern': pattern,
                    'score': match_count,
                    'matched_keywords': matched_keywords
                })
        
        self.matches.sort(key=lambda x: x['score'], reverse=True)
        return self.matches
    
    def extract_error_lines(self, log_file, context_lines=2):
        """
        Extract error lines with surrounding context from log.
        """
        error_snippets = []
        with open(log_file, 'r') as f:
            lines = f.readlines()
        
        for i, line in enumerate(lines):
            if 'ERROR' in line or 'FATAL' in line:
                start = max(0, i - context_lines)
                end = min(len(lines), i + context_lines + 1)
                snippet = ''.join(lines[start:end])
                error_snippets.append(snippet)
        
        return error_snippets
    
    def generate_report(self, log_file):
        """
        Generate a comprehensive triage report.
        """
        print(f"\n{Fore.CYAN}{'='*70}")
        print(f"{Fore.CYAN}CI FAILURE TRIAGE REPORT")
        print(f"{Fore.CYAN}{'='*70}\n")
        
        print(f"{Fore.YELLOW}Log File: {Fore.WHITE}{log_file}\n")
        
        if not self.matches:
            print(f"{Fore.RED}No known failure patterns detected.")
            print(f"{Fore.YELLOW}Manual investigation required.\n")
            return
        
        print(f"{Fore.GREEN}Detected Failure Patterns:\n")
        
        for idx, match in enumerate(self.matches, 1):
            pattern = match['pattern']
            severity_color = self._get_severity_color(pattern['severity'])
            
            print(f"{Fore.WHITE}{idx}. {Fore.CYAN}{pattern['name']}")
            print(f"   {Fore.WHITE}Severity: {severity_color}{pattern['severity'].upper()}")
            print(f"   {Fore.WHITE}Confidence Score: {Fore.YELLOW}{match['score']}")
            print(f"   {Fore.WHITE}Matched Keywords: {Fore.MAGENTA}{', '.join(match['matched_keywords'])}\n")
            
            print(f"   {Fore.GREEN}Suggested Actions:")
            for suggestion in pattern['suggestions']:
                print(f"   {Fore.WHITE}- {suggestion}")
            print()
        
        print(f"{Fore.YELLOW}Error Context from Log:\n")
        error_snippets = self.extract_error_lines(log_file)
        
        for snippet in error_snippets[:3]:
            print(f"{Fore.RED}{snippet}")
            print(f"{Fore.WHITE}{'-'*70}\n")
    
    def _get_severity_color(self, severity):
        colors = {
            'critical': Fore.RED,
            'high': Fore.RED,
            'medium': Fore.YELLOW,
            'low': Fore.GREEN
        }
        return colors.get(severity.lower(), Fore.WHITE)

def main():
    if len(sys.argv) < 2:
        print(f"{Fore.RED}Usage: python3 ci_triage.py <log_file>")
        sys.exit(1)
    
    log_file = sys.argv[1]
    patterns_file = "patterns/failure_patterns.yaml"
    
    if not Path(log_file).exists():
        print(f"{Fore.RED}Error: Log file not found: {log_file}")
        sys.exit(1)
    
    assistant = CITriageAssistant(patterns_file)
    assistant.analyze_log(log_file)
    assistant.generate_report(log_file)

if __name__ == "__main__":
    main()
