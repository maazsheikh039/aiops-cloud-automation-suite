"""Helper utilities for opsctl."""

import sys

def print_success(message):
    """Print success message in green."""
    print(f"\033[92m[SUCCESS] {message}\033[0m")

def print_error(message):
    """Print error message in red."""
    print(f"\033[91m[ERROR] {message}\033[0m", file=sys.stderr)

def print_info(message):
    """Print info message in blue."""
    print(f"\033[94m[INFO] {message}\033[0m")

def validate_environment(env):
    """Validate environment parameter."""
    allowed_envs = ['dev', 'staging', 'prod']
    return env in allowed_envs
