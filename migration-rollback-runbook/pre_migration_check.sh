#!/bin/bash

source db_config.sh

echo "=== Pre-Migration Checklist ==="
echo "Timestamp: $(date)"
echo ""

check_db_connection() {
    PGPASSWORD="$PGPASSWORD" psql -h "$PGHOST" -p "$PGPORT" -U "$PGUSER" -d "$PGDATABASE" -c "SELECT 1;" > /dev/null 2>&1
    if [ $? -eq 0 ]; then
        echo "[PASS] Database connection successful."
        return 0
    else
        echo "[FAIL] Database connection failed."
        return 1
    fi
}

verify_backup_exists() {
    local backup_dir="backups"
    if [ -d "$backup_dir" ] && [ "$(find "$backup_dir" -name "*.sql" -mtime -1 2>/dev/null)" ]; then
        echo "[PASS] Recent backup found within the last 24 hours."
        return 0
    else
        echo "[WARN] No recent backup found within the last 24 hours."
        return 1
    fi
}

check_disk_space() {
    local avail_space=$(df -m . | awk 'NR==2 {print $4}')
    if [ "$avail_space" -gt 100 ]; then
        echo "[PASS] Sufficient disk space available (${avail_space}MB free)."
        return 0
    else
        echo "[FAIL] Low disk space (${avail_space}MB free)."
        return 1
    fi
}

check_active_connections() {
    local conn_count=$(PGPASSWORD="$PGPASSWORD" psql -h "$PGHOST" -p "$PGPORT" -U "$PGUSER" -d "$PGDATABASE" -t -c "SELECT count(*) FROM pg_stat_activity WHERE datname = '$PGDATABASE';")
    echo "[INFO] Active connections to $PGDATABASE: $(echo $conn_count | tr -d ' ')"
}

echo "1. Database Connection..."
check_db_connection

echo "2. Backup Status..."
verify_backup_exists

echo "3. Disk Space..."
check_disk_space

echo "4. Active Connections..."
check_active_connections

echo ""
echo "=== Checklist Complete ==="
