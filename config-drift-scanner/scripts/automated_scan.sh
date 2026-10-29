#!/bin/bash

echo "Running automated drift scan..."
./scripts/capture_current.sh
python3 scripts/drift_scanner.py

DRIFT_COUNT=$(cat reports/drift_report_*.json | tail -1 | jq '.drifts_detected')

if [ "$DRIFT_COUNT" -gt 0 ]; then
    echo "WARNING: $DRIFT_COUNT configuration drift(s) detected!"
    exit 1
else
    echo "No configuration drift detected."
    exit 0
fi
