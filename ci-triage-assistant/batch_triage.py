#!/usr/bin/env python3
"""
Batch CI Log Analyzer
Processes multiple log files and generates summary report
"""

import sys
from pathlib import Path
from ci_triage import CITriageAssistant
from colorama import Fore, init

init(autoreset=True)

def analyze_directory(log_dir, patterns_file):
    log_files = list(Path(log_dir).glob("*.log"))
    
    if not log_files:
        print(f"{Fore.RED}No log files found in {log_dir}")
        return
    
    print(f"{Fore.CYAN}Analyzing {len(log_files)} log files...\n")
    
    assistant = CITriageAssistant(patterns_file)
    results = []
    
    for log_file in log_files:
        matches = assistant.analyze_log(str(log_file))
        results.append({
            'file': log_file.name,
            'matches': matches
        })
    
    print(f"{Fore.CYAN}{'='*70}")
    print(f"{Fore.CYAN}BATCH ANALYSIS SUMMARY")
    print(f"{Fore.CYAN}{'='*70}\n")
    
    for result in results:
        print(f"{Fore.YELLOW}{result['file']}")
        if result['matches']:
            top_match = result['matches'][0]
            print(f"  {Fore.GREEN}Top Issue: {top_match['pattern']['name']}")
            print(f"  {Fore.WHITE}Severity: {top_match['pattern']['severity']}\n")
        else:
            print(f"  {Fore.RED}No patterns detected\n")

if __name__ == "__main__":
    log_dir = sys.argv[1] if len(sys.argv) > 1 else "logs"
    patterns_file = "patterns/failure_patterns.yaml"
    analyze_directory(log_dir, patterns_file)
