#!/bin/bash

# Configuration Baseline Capture Script
BASELINE_DIR="$HOME/config-drift-scanner/baselines"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)

mkdir -p "$BASELINE_DIR"

capture_system_config() {
    echo "Capturing baseline configuration..."
    
    # Capture /etc/hosts
    cp /etc/hosts "$BASELINE_DIR/hosts.baseline"
    
    # Capture package list
    dpkg -l > "$BASELINE_DIR/packages.baseline"
    
    # Capture running services
    systemctl list-units --type=service --state=running > "$BASELINE_DIR/services.baseline"
    
    # Capture network interfaces
    ip addr show > "$BASELINE_DIR/network.baseline"
    
    # Capture environment variables (user-level)
    env | sort > "$BASELINE_DIR/environment.baseline"
    
    echo "Baseline captured successfully at: $BASELINE_DIR"
}

capture_system_config
