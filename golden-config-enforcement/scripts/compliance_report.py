#!/usr/bin/env python3
"""
Generate compliance report from logs
"""

import json
from pathlib import Path

def generate_report(log_dir):
    log_path = Path(log_dir)
    log_files = list(log_path.glob("violations_*.json"))
    
    print("\n" + "="*50)
    print(" COMPLIANCE AUDIT REPORT")
    print("="*50)
    print(f" Total Violation Logs Found: {len(log_files)}")
    
    for file in log_files:
        with open(file, 'r') as f:
            data = json.load(f)
            print(f"\n - Config: {data.get('config_name')}")
            print(f"   Security Violations: {len(data.get('security_violations', []))}")
            for sv in data.get('security_violations', []):
                print(f"     * {sv}")
    print("="*50 + "\n")

if __name__ == "__main__":
    generate_report('logs')
