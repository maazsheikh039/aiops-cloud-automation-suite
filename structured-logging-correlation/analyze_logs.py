import json
import sys
from collections import defaultdict

def analyze_logs(log_file):
    """Analyze structured logs and group by correlation ID."""
    correlation_groups = defaultdict(list)
    
    try:
        with open(log_file, 'r') as f:
            for line in f:
                try:
                    log_entry = json.loads(line.strip())
                    corr_id = log_entry.get('correlation_id', 'unknown')
                    correlation_groups[corr_id].append(log_entry)
                except json.JSONDecodeError:
                    continue
    except FileNotFoundError:
        print(f"Error: Log file {log_file} not found.")
        sys.exit(1)
        
    print("\n" + "="*60)
    print(" DISTRIBUTED TRACE ANALYSIS BY CORRELATION ID")
    print("="*60)
    
    for corr_id, entries in correlation_groups.items():
        print(f"\nCorrelation ID: {corr_id} (Total Events: {len(entries)})")
        for entry in entries:
            timestamp = entry.get('asctime', entry.get('timestamp', 'N/A'))
            level = entry.get('levelname', entry.get('level', 'INFO'))
            msg = entry.get('message', '')
            print(f"  [{timestamp}] {level}: {msg}")
            
    print("="*60 + "\n")

if __name__ == '__main__':
    if len(sys.argv) > 1:
        analyze_logs(sys.argv[1])
    else:
        print("Usage: python analyze_logs.py <log_file>")
