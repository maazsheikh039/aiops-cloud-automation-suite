#!/usr/bin/env python3
import json
import os
from datetime import datetime
from pathlib import Path

class AuditLogger:
    def __init__(self, log_directory="logs"):
        self.log_directory = Path(log_directory)
        self.log_directory.mkdir(parents=True, exist_ok=True)
        today_str = datetime.now().strftime("%Y-%m-%d")
        self.log_file = self.log_directory / f"audit_{today_str}.log"
    
    def log_event(self, event_type, event_data):
        record = {
            "timestamp": datetime.now().isoformat(),
            "event_type": event_type,
            "data": event_data
        }
        with open(self.log_file, 'a', encoding='utf-8') as f:
            f.write(json.dumps(record) + "\n")
    
    def query_logs(self, filters=None):
        records = []
        if not self.log_file.exists():
            return records
            
        with open(self.log_file, 'r', encoding='utf-8') as f:
            for line in f:
                if line.strip():
                    try:
                        records.append(json.loads(line))
                    except json.JSONDecodeError:
                        continue
        
        if not filters:
            return records
            
        filtered = []
        for rec in records:
            match = True
            if filters.get('event_type') and rec.get('event_type') != filters['event_type']:
                match = False
            if filters.get('user') and rec.get('data', {}).get('requester') != filters['user'] and rec.get('data', {}).get('approver') != filters['user']:
                match = False
            if match:
                filtered.append(rec)
        return filtered

    def generate_report(self, start_date, end_date):
        records = self.query_logs()
        total_events = len(records)
        event_counts = {}
        for rec in records:
            et = rec.get('event_type', 'unknown')
            event_counts[et] = event_counts.get(et, 0) + 1
            
        return {
            "total_events": total_events,
            "event_breakdown": event_counts,
            "start_date": str(start_date),
            "end_date": str(end_date)
        }
