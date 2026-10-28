"""Configuration command implementation."""

import json
import os
from opsctl.utils.helpers import print_success, print_error

CONFIG_FILE = os.path.expanduser('~/.opsctl/config.json')

def load_config():
    if not os.path.exists(CONFIG_FILE):
        return {}
    try:
        with open(CONFIG_FILE, 'r') as f:
            return json.load(f)
    except Exception:
        return {}

def save_config(config):
    os.makedirs(os.path.dirname(CONFIG_FILE), exist_ok=True)
    with open(CONFIG_FILE, 'w') as f:
        json.dump(config, f, indent=2)

def execute(args):
    """Execute the config command."""
    config = load_config()
    
    if args.action == 'get':
        if args.key in config:
            print(config[args.key])
            return 0
        else:
            print_error(f"Config key '{args.key}' not found.")
            return 1
            
    elif args.action == 'set':
        if not args.value:
            print_error("Value is required for 'set' action.")
            return 1
        config[args.key] = args.value
        save_config(config)
        print_success(f"Configured '{args.key}' = '{args.value}'")
        return 0
        
    return 1

def add_parser(subparsers):
    """Add config command parser."""
    parser = subparsers.add_parser('config', help='Manage configuration')
    sub_subparsers = parser.add_subparsers(dest='action', required=True)
    
    # Get action
    get_parser = sub_subparsers.add_parser('get', help='Get configuration value')
    get_parser.add_argument('key', type=str, help='Configuration key')
    get_parser.set_defaults(func=execute)
    
    # Set action
    set_parser = sub_subparsers.add_parser('set', help='Set configuration value')
    set_parser.add_argument('key', type=str, help='Configuration key')
    set_parser.add_argument('value', type=str, help='Configuration value')
    set_parser.set_defaults(func=execute)
