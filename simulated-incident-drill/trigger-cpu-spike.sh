#!/bin/bash
# Simulates CPU spike using stress-ng

echo "Triggering CPU spike incident..."
stress-ng --cpu 4 --timeout 120s &
echo "CPU spike incident triggered (PID: $!)"
