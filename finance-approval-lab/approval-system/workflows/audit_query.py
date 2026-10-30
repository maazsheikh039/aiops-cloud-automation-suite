#!/usr/bin/env python3
import argparse
import json
from datetime import datetime, timedelta
from audit_logger import AuditLogger

def main():
    parser = argparse.ArgumentParser(description='Audit Log Query Tool')
    parser.add_argument('--days', type=int, default=7, help='Days to look back')
    parser.add_argument('--event-type', help='Filter by event type')
    parser.add_argument('--user', help='Filter by username')
    parser.add_argument('--report', action='store_true', help='Generate report')
    
    args = parser.parse_args()
    logger = AuditLogger()
    
    if args.report:
        start_date = datetime.now() - timedelta(days=args.days)
        end_date = datetime.now()
        report = logger.generate_report(start_date, end_date)
        print("=== AUDIT SUMMARY REPORT ===")
        print(json.dumps(report, indent=2))
    else:
        filters = {}
        if args.event_type:
            filters['event_type'] = args.event_type
        if args.user:
            filters['user'] = args.user
            
        logs = logger.query_logs(filters)
        print(f"Found {len(logs)} audit record(s):")
        for log in logs:
            print(json.dumps(log))

if __name__ == '__main__':
    main()
