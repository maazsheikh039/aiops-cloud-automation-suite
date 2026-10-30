#!/usr/bin/env python3
"""
Compliance Evidence Collector
Collects system evidence for compliance reporting
"""

import json
import yaml
import subprocess
from datetime import datetime
from pathlib import Path

class EvidenceCollector:
    def __init__(self, config_path):
        with open(config_path, 'r') as f:
            self.config = yaml.safe_load(f)
        self.output_dir = Path('../output')
        self.output_dir.mkdir(parents=True, exist_ok=True)
    
    def collect_system_logs(self):
        evidence = {
            'timestamp': datetime.now().isoformat(),
            'evidence_type': 'system_logs',
            'data': []
        }
        try:
            res = subprocess.run(['journalctl', '-n', '50', '--no-pager'], capture_output=True, text=True, timeout=10)
            logs = res.stdout.splitlines() if res.returncode == 0 else ["Journalctl unavailable"]
        except Exception:
            logs = ["Could not retrieve journal logs"]
            
        try:
            svc_res = subprocess.run(['systemctl', 'list-units', '--type=service', '--state=running', '--no-pager'], capture_output=True, text=True, timeout=10)
            services = svc_res.stdout.splitlines() if svc_res.returncode == 0 else []
        except Exception:
            services = []
            
        evidence['data'] = {
            'recent_journal_logs': logs[:50],
            'running_services_sample': services[:30]
        }
        return evidence
    
    def collect_access_logs(self):
        evidence = {
            'timestamp': datetime.now().isoformat(),
            'evidence_type': 'access_logs',
            'data': {}
        }
        try:
            last_res = subprocess.run(['last', '-n', '20'], capture_output=True, text=True, timeout=5)
            evidence['data']['last_logins'] = last_res.stdout.splitlines() if last_res.returncode == 0 else []
        except Exception:
            evidence['data']['last_logins'] = []
            
        try:
            who_res = subprocess.run(['who'], capture_output=True, text=True, timeout=5)
            evidence['data']['current_users'] = who_res.stdout.splitlines() if who_res.returncode == 0 else []
        except Exception:
            evidence['data']['current_users'] = []
            
        return evidence
    
    def collect_configuration_snapshot(self):
        evidence = {
            'timestamp': datetime.now().isoformat(),
            'evidence_type': 'configuration_snapshots',
            'data': {}
        }
        try:
            ip_res = subprocess.run(['ip', 'addr'], capture_output=True, text=True, timeout=5)
            evidence['data']['network_config'] = ip_res.stdout if ip_res.returncode == 0 else "Unavailable"
        except Exception:
            evidence['data']['network_config'] = "Unavailable"
            
        try:
            pkg_res = subprocess.run(['dpkg', '-l'], capture_output=True, text=True, timeout=10)
            packages = pkg_res.stdout.splitlines()[:50] if pkg_res.returncode == 0 else []
            evidence['data']['installed_packages_sample'] = packages
        except Exception:
            evidence['data']['installed_packages_sample'] = []
            
        return evidence
