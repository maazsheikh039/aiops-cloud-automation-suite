#!/usr/bin/env python3
"""
Incident logging and documentation system
"""
import json
import datetime
from pathlib import Path

class IncidentLogger:
    def __init__(self, log_dir="incident-logs"):
        self.log_dir = Path(log_dir)
        self.log_dir.mkdir(exist_ok=True)
    
    def start_incident(self, incident_type, severity):
        """Start a new incident and create log file."""
        timestamp = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
        incident_id = f"INC-{timestamp}"
        incident_file = self.log_dir / f"{incident_id}.json"
        
        incident_data = {
            "incident_id": incident_id,
            "type": incident_type,
            "severity": severity,
            "status": "Investigating",
            "start_time": datetime.datetime.now().isoformat(),
            "actions": [],
            "resolution": None,
            "root_cause": None,
            "end_time": None
        }
        
        with open(incident_file, 'w') as f:
            json.dump(incident_data, f, indent=2)
            
        print(f"Incident started: {incident_id}")
        return incident_id
    
    def log_action(self, incident_id, action, result):
        """Log an action taken during incident response."""
        incident_file = self.log_dir / f"{incident_id}.json"
        if not incident_file.exists():
            print(f"Incident {incident_id} not found.")
            return
            
        with open(incident_file, 'r') as f:
            data = json.load(f)
            
        data["actions"].append({
            "timestamp": datetime.datetime.now().isoformat(),
            "action": action,
            "result": result
        })
        
        with open(incident_file, 'w') as f:
            json.dump(data, f, indent=2)
    
    def close_incident(self, incident_id, resolution, root_cause):
        """Close an incident with resolution details."""
        incident_file = self.log_dir / f"{incident_id}.json"
        if not incident_file.exists():
            return
            
        with open(incident_file, 'r') as f:
            data = json.load(f)
            
        data["status"] = "Resolved"
        data["end_time"] = datetime.datetime.now().isoformat()
        data["resolution"] = resolution
        data["root_cause"] = root_cause
        
        with open(incident_file, 'w') as f:
            json.dump(data, f, indent=2)
        print(f"Incident {incident_id} closed successfully.")

if __name__ == "__main__":
    logger = IncidentLogger()
    print("Incident Logger initialized successfully.")
