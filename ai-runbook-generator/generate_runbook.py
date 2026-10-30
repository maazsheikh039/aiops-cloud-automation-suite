#!/usr/bin/env python3
from collect_context import SystemContextCollector
from runbook_generator import RunbookGenerator
import sys

def main():
    scenarios = {
        "high_cpu": "CPU usage is at 95% and application is slow",
        "disk_full": "Root filesystem is 98% full",
        "service_down": "Web service is not responding to requests"
    }
    
    scenario_key = sys.argv[1] if len(sys.argv) > 1 else "high_cpu"
    if scenario_key not in scenarios:
        print(f"Invalid scenario. Choose from: {list(scenarios.keys())}")
        sys.exit(1)
        
    scenario_desc = scenarios[scenario_key]
    print(f"=== Starting Runbook Generation for Scenario: {scenario_key} ===")
    
    print("[1/4] Collecting system context...")
    collector = SystemContextCollector()
    collector.collect_system_info()
    collector.collect_service_status(['ssh', 'cron'])
    collector.collect_network_info()
    collector.collect_disk_info()
    context_file = collector.export_context()
    
    print("[2/4] Initializing AI Runbook Generator...")
    generator = RunbookGenerator()
    context = generator.load_context(context_file)
    
    print("[3/4] Generating AI remediation steps via local model (llama3.2:1b)...")
    prompt = generator.create_prompt(context, scenario_desc)
    ai_output = generator.generate_with_ai(prompt)
    
    print("[4/4] Formatting and exporting runbook...")
    runbook_data = generator.format_runbook(ai_output, context, scenario_desc)
    generator.export_runbook(runbook_data, scenario_key)
    
    print("Runbook generated successfully!")

if __name__ == "__main__":
    main()
