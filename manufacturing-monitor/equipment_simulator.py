#!/usr/bin/env python3
"""
Manufacturing Equipment Simulator
Generates realistic telemetry data for production machines
"""

import time
import random
from datetime import datetime
from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS

class EquipmentSimulator:
    def __init__(self, equipment_id, equipment_type):
        self.equipment_id = equipment_id
        self.equipment_type = equipment_type
        self.is_running = True
        
        # Initialize InfluxDB client connection (InfluxDB 1.x compatibility)
        self.client = InfluxDBClient(url="http://localhost:8086", token="admin:admin123", org="-")
        self.write_api = self.client.write_api(write_options=SYNCHRONOUS)
        self.bucket = "manufacturing/autogen"

    def generate_telemetry(self):
        """Generate realistic telemetry metrics."""
        # Simulate occasional downtime (5% chance of error status)
        status_choice = random.choices(["running", "idle", "error"], weights=[85, 10, 5])[0]
        
        temperature = round(random.uniform(60.0, 95.0), 2)
        pressure = round(random.uniform(20.0, 50.0), 2)
        speed = round(random.uniform(0.0, 100.0), 2) if status_choice == "running" else 0.0
        
        if status_choice == "error":
            temperature = round(random.uniform(98.0, 115.0), 2)  # overheating during error
            
        return {
            "temperature": temperature,
            "pressure": pressure,
            "speed": speed,
            "status": status_choice
        }

    def send_telemetry(self, telemetry_data):
        """Send telemetry point to InfluxDB."""
        try:
            point = Point("equipment_metrics") \
                .tag("equipment_id", self.equipment_id) \
                .tag("equipment_type", self.equipment_type) \
                .field("temperature", float(telemetry_data["temperature"])) \
                .field("pressure", float(telemetry_data["pressure"])) \
                .field("speed", float(telemetry_data["speed"])) \
                .field("status_str", str(telemetry_data["status"])) \
                .time(datetime.utcnow())
                
            # Write point using legacy database/retention policy mapping for InfluxDB 1.x
            self.write_api.write(bucket="manufacturing/autogen", record=point)
        except Exception as e:
            print(f"Error writing to InfluxDB: {e}")

    def run(self, duration=300):
        """Run simulator loop."""
        print(f"Starting equipment simulator for {self.equipment_id} ({self.equipment_type})...")
        start_time = time.time()
        try:
            while self.is_running:
                if time.time() - start_time > duration:
                    break
                data = self.generate_telemetry()
                self.send_telemetry(data)
                print(f"[{datetime.now().strftime('%H:%M:%S')}] Sent telemetry for {self.equipment_id}: {data}")
                time.sleep(5)
        except KeyboardInterrupt:
            print("Simulator stopped by user.")

if __name__ == "__main__":
    simulator = EquipmentSimulator("MACHINE-001", "CNC_MILL")
    simulator.run()

