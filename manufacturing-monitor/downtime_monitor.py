#!/usr/bin/env python3
"""
Manufacturing Downtime Monitor
Detects equipment downtime and sends alerts
"""

import time
import requests
from datetime import datetime, timedelta
from influxdb_client import InfluxDBClient
from pathlib import Path

class DowntimeMonitor:
    def __init__(self, check_interval=10):
        self.check_interval = check_interval
        self.downtime_threshold = 30  # seconds
        self.alert_cooldown = {}  # Track last alert time per equipment
        self.alert_log_path = Path("/tmp/manufacturing_alerts.log")
        
        # Initialize InfluxDB query client
        self.client = InfluxDBClient(url="http://localhost:8086", token="admin:admin123", org="-")
        self.query_api = self.client.query_api()
        
    def query_equipment_status(self, equipment_id, time_window="1m"):
        """Query recent equipment status from InfluxDB."""
        query = f'''
        from(bucket: "manufacturing/autogen")
          |> range(start: -{time_window})
          |> filter(fn: (r) => r["_measurement"] == "equipment_metrics")
          |> filter(fn: (r) => r["equipment_id"] == "{equipment_id}")
          |> filter(fn: (r) => r["_field"] == "status_str" or r["_field"] == "temperature")
          |> last()
        '''
        try:
            tables = self.query_api.query(query)
            records = []
            for table in tables:
                for record in table.records:
                    records.append({
                        "field": record.get_field(),
                        "value": record.get_value(),
                        "time": record.get_time()
                    })
            return records
        except Exception as e:
            print(f"Error querying InfluxDB for {equipment_id}: {e}")
            return []
    
    def detect_downtime(self, equipment_id):
        """Detect if equipment is experiencing downtime or error status."""
        records = self.query_equipment_status(equipment_id, time_window="45s")
        if not records:
            return True, "No telemetry data received (Equipment Offline)"
            
        for rec in records:
            if rec["field"] == "status_str" and rec["value"] == "error":
                return True, "Equipment reported 'error' status (Potential Failure)"
                
        return False, "Operational"
    
    def send_alert(self, equipment_id, reason):
        """Send downtime alert respecting cooldown periods (5 minutes)."""
        now = datetime.now()
        if equipment_id in self.alert_cooldown:
            last_alert = self.alert_cooldown[equipment_id]
            if now - last_alert < timedelta(minutes=5):
                return # In cooldown
                
        self.alert_cooldown[equipment_id] = now
        log_entry = f"{now.isoformat()} | ALERT | Equipment: {equipment_id} | Reason: {reason}\n"
        print(log_entry.strip())
        
        with open(self.alert_log_path, "a", encoding="utf-8") as f:
            f.write(log_entry)
            
    def monitor(self, equipment_list):
        """Main continuous monitoring loop."""
        print(f"Starting Manufacturing Downtime Monitor for: {equipment_list}")
        try:
            while True:
                for eq_id in equipment_list:
                    is_down, reason = self.detect_downtime(eq_id)
                    if is_down:
                        self.send_alert(eq_id, reason)
                    else:
                        print(f"[{datetime.now().strftime('%H:%M:%S']}] {eq_id}: OK")
                time.sleep(self.check_interval)
        except KeyboardInterrupt:
            print("Downtime monitor stopped.")

if __name__ == "__main__":
    monitor = DowntimeMonitor(check_interval=10)
    equipment_to_monitor = ["MACHINE-001", "MACHINE-002"]
    monitor.monitor(equipment_to_monitor)
