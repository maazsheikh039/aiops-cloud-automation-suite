#!/bin/bash
"""
Pre-deployment enforcement hook
Runs before any configuration deployment
"""

echo "Running Golden Configuration Enforcement..."
echo "=========================================="

python3 scripts/config_enforcer.py

if [ $? -eq 0 ]; then
    echo "All configurations compliant. Deployment allowed."
    exit 0
else
    echo "Configuration violations detected. Deployment blocked."
    exit 1
fi
