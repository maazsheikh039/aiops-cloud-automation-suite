#!/usr/bin/env python3
"""
Dependency security and policy checker
"""
import subprocess
import sys

if __name__ == '__main__':
    print("Running dependency security checks...")
    
    print("\n[1/2] Checking for known vulnerabilities with safety...")
    safety_res = subprocess.run(['safety', 'check', '--json'], check=False)
    
    print("\n[2/2] Running pip-audit for CVE scanning...")
    audit_res = subprocess.run(['pip-audit', '--desc'], check=False)
    
    if safety_res.returncode != 0 or audit_res.returncode != 0:
        print("\nWARNING: Vulnerabilities or security issues detected!")
    else:
        print("\nSUCCESS: No critical vulnerabilities found.")
