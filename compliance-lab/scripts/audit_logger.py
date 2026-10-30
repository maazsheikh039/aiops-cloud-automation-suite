#!/usr/bin/env python3
"""
Audit Log Generator
Creates structured audit logs for compliance tracking
"""

import json
from datetime import datetime
from pathlib import Path

class AuditLogger:
    def __init__(self, log_dir='../logs'):
        self.log_dir = Path(log_dir)
        self.log_dir.mkdir(parents=True, exist_ok=True)
        self.log_file = self.log_dir / 'audit.log'
        self.json_log_file = self.log_dir / 'audit.json'
    
    def log_evidence_collection(self, evidence_type, status, details=None):
        entry = {
            'timestamp': datetime.now().isoformat(),
            'event_type': 'evidence_collection',
            'evidence_type': evidence_type,
            'status': status,
            'details': details or {}
        }
        self._write_entry(entry)
    
    def log_report_generation(self, report_type, output_path, status):
        entry = {
            'timestamp': datetime.now().isoformat(),
            'event_type': 'report_generation',
            'report_type': report_type,
            'output_path': output_path,
            'status': status
        }
        self._write_entry(entry)
        
    def _write_entry(self, entry):
        with open(self.log_file, 'a', encoding='utf-8') as f:
            f.write(f"[{entry['timestamp']}] {entry['event_type'].upper()} - Type: {entry.get('evidence_type') or entry.get('report_type')} - Status: {entry['status']}\n")
            
        with open(self.json_log_file, 'a', encoding='utf-8') as f:
            f.write(json.dumps(entry) + '\n')
            
    def generate_audit_summary(self):
        records = []
        if self.json_log_file.exists():
            with open(self.json_log_file, 'r', encoding='utf-8') as f:
                for line in f:
                    if line.strip():
                        try:
                            records.append(json.loads(line))
                        except Exception:
                            pass
        return {
            'total_audit_events': len(records),
            'records': records
        }
