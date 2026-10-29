#!/bin/bash
# Safe dependency upgrade testing script

set -e
BACKUP_DIR="backup_$(date +%Y%m%d_%H%M%S)"

echo "=== Dependency Upgrade Testing ==="

backup_environment() {
    echo "[1/4] Backing up current environment..."
    mkdir -p "$BACKUP_DIR"
    cp requirements.txt "$BACKUP_DIR/"
    pip freeze > "$BACKUP_DIR/frozen_requirements.txt"
    echo "Backup created in $BACKUP_DIR"
}

run_tests() {
    echo "[2/4] Running test suite..."
    pytest tests/ -v
}

security_scan() {
    echo "[3/4] Running security scan..."
    python3 check_dependencies.py
}

rollback_if_failed() {
    if [ $? -ne 0 ]; then
        echo "[4/4] Tests failed! Rolling back..."
        cp "$BACKUP_DIR/requirements.txt" requirements.txt
        pip install -r requirements.txt
        echo "Rollback completed successfully."
        exit 1
    else
        echo "[4/4] All tests passed! Upgrade validation successful."
    fi
}

backup_environment
run_tests
security_scan
rollback_if_failed

echo "=== Upgrade testing complete ==="
