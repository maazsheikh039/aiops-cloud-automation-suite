#!/bin/bash
# Simulates disk space exhaustion safely in /tmp

FILL_DIR="/tmp/disk-fill-test"
mkdir -p $FILL_DIR

echo "Triggering disk space incident..."
# Create a 500MB file using dd
dd if=/dev/zero of="$FILL_DIR/large_payload.img" bs=1M count=500 status=progress

echo "Disk space incident triggered"
df -h
