#!/usr/bin/env python3
"""
Main CLI entry point for opsctl.
Handles argument parsing and command routing.
"""

import argparse
import sys
from opsctl.version import __version__, __description__
from opsctl.commands import status, deploy, config


def create_parser():
    """Create and configure the argument parser."""
    parser = argparse.ArgumentParser(
        prog='opsctl',
        description=__description__,
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    parser.add_argument(
        '--version',
        action='version',
        version=f'%(prog)s {__version__}'
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Add subcommands using modular add_parser functions
    status.add_parser(subparsers)
    deploy.add_parser(subparsers)
    config.add_parser(subparsers)
    
    return parser


def main():
    """Main entry point for the CLI application."""
    parser = create_parser()
    args = parser.parse_args()
    
    if not hasattr(args, 'func'):
        parser.print_help()
        sys.exit(1)
        
    try:
        exit_code = args.func(args)
        sys.exit(exit_code)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
