"""Status command implementation."""

import json
import time

def execute(args):
    """Execute the status command."""
    status_data = {
        "service": args.service if args.service else "all-services",
        "status": "healthy",
        "uptime": "99.9%",
        "timestamp": time.time()
    }
    
    if args.format == 'json':
        print(json.dumps(status_data, indent=2))
    else:
        print(f"Service: {status_data['service']}")
        print(f"Status: {status_data['status']}")
        print(f"Uptime: {status_data['uptime']}")
    return 0

def add_parser(subparsers):
    """Add status command parser."""
    parser = subparsers.add_parser('status', help='Check system status')
    parser.add_argument('--service', type=str, help='Specific service to check')
    parser.add_argument('--format', choices=['text', 'json'], default='text', help='Output format')
    parser.set_defaults(func=execute)
