#!/usr/init/env python3
"""
Golden Configuration Enforcement System
Compares current configurations against golden standards
"""

import yaml
import json
import sys
from pathlib import Path
from deepdiff import DeepDiff
from datetime import datetime

class ConfigEnforcer:
    def __init__(self, golden_dir, current_dir, log_dir):
        self.golden_dir = Path(golden_dir)
        self.current_dir = Path(current_dir)
        self.log_dir = Path(log_dir)
        self.log_dir.mkdir(parents=True, exist_ok=True)
        self.violations = []
        
    def load_yaml(self, filepath):
        """Load YAML configuration file with error handling."""
        try:
            with open(filepath, 'r') as f:
                return yaml.safe_load(f)
        except Exception as e:
            print(f"Error loading YAML file {filepath}: {e}")
            return None
    
    def compare_configs(self, golden_config, current_config, config_name):
        """Compare current config against golden standard using DeepDiff."""
        diff = DeepDiff(golden_config, current_config, ignore_order=True)
        violations = []
        
        if diff:
            diff_dict = json.loads(diff.to_json())
            violations.append({
                "config": config_name,
                "timestamp": datetime.now().isoformat(),
                "differences": diff_dict
            })
        return violations
    
    def check_security_violations(self, current_config, config_name):
        """Check for critical security policy violations."""
        security_violations = []
        security = current_config.get("security", {})
        
        if security.get("permit_root_login") is True:
            security_violations.append(f"CRITICAL: Root login is permitted in {config_name}")
        if security.get("password_authentication") is True:
            security_violations.append(f"WARNING: Password authentication is enabled in {config_name}")
        if "ssl" in security and security["ssl"].get("enabled") is False:
            security_violations.append(f"CRITICAL: SSL encryption is disabled in {config_name}")
            
        return security_violations
    
    def log_violations(self, violations, security_violations, config_name):
        """Log violations to a timestamped file and print summary."""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        log_file = self.log_dir / f"violations_{config_name}_{timestamp}.json"
        
        log_data = {
            "config_name": config_name,
            "violations": violations,
            "security_violations": security_violations
        }
        
        with open(log_file, 'w') as f:
            json.dump(log_data, f, indent=2)
            
        print(f"Log written to {log_file}")
    
    def block_deployment(self, config_name, reasons):
        """Block deployment due to violations."""
        print(f"\n{'='*60}")
        print(f"DEPLOYMENT BLOCKED: {config_name}")
        print(f"{'='*60}")
        for r in reasons:
            print(f" - {r}")
        print(f"{'='*60}\n")
    
    def enforce_all(self):
        """Enforce compliance across all current configuration files."""
        all_compliant = True
        
        # Map current files to corresponding golden baselines
        mapping = {
            "webserver_compliant.yaml": "webserver_golden.yaml",
            "ssh_current.yaml": "ssh_golden.yaml"
        }
        
        for curr_filename, golden_filename in mapping.items():
            curr_path = self.current_dir / curr_filename
            golden_path = self.golden_dir / golden_filename
            
            if not curr_path.exists():
                print(f"Skipping {curr_filename}: file not found in current directory.")
                continue
                
            if not golden_path.exists():
                print(f"Golden standard {golden_filename} missing for {curr_filename}.")
                all_compliant = False
                continue
                
            curr_config = self.load_yaml(curr_path)
            golden_config = self.load_yaml(golden_path)
            
            if not curr_config or not golden_config:
                all_compliant = False
                continue
                
            violations = self.compare_configs(golden_config, curr_config, curr_filename)
            sec_violations = self.check_security_violations(curr_config, curr_filename)
            
            if violations or sec_violations:
                all_compliant = False
                self.log_violations(violations, sec_violations, curr_filename)
                reasons = [str(v) for v in violations] + sec_violations
                self.block_deployment(curr_filename, reasons)
            else:
                print(f"[PASSED] {curr_filename} matches golden standard and security policies.")
                
        return all_compliant

def main():
    enforcer = ConfigEnforcer(
        golden_dir='golden',
        current_dir='current',
        log_dir='logs'
    )
    
    compliant = enforcer.enforce_all()
    sys.exit(0 if compliant else 1)

if __name__ == "__main__":
    main()
