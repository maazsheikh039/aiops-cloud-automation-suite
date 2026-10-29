#!/bin/bash

source db_config.sh

MIGRATION_DIR="migrations"
LOG_DIR="logs"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)

mkdir -p "$LOG_DIR"

log_message() {
    local level=$1
    local message=$2
    local log_entry="[$(date +'%Y-%m-%d %H:%M:%S')] [$level] $message"
    echo "$log_entry"
    echo "$log_entry" >> "$LOG_DIR/migration_$TIMESTAMP.log"
}

execute_migration() {
    local migration_name=$1
    local direction=$2  # 'up' or 'down'
    local migration_file="$MIGRATION_DIR/$direction/$migration_name.sql"
    
    if [ ! -f "$migration_file" ]; then
        log_message "ERROR" "Migration file not found: $migration_file"
        return 1
    fi
    
    log_message "INFO" "Starting $direction migration for: $migration_name"
    
    # Execute SQL using psql within a transaction or script-defined blocks
    PGPASSWORD="$PGPASSWORD" psql -h "$PGHOST" -p "$PGPORT" -U "$PGUSER" -d "$PGDATABASE" -f "$migration_file"
    local exit_code=$?
    
    if [ $exit_code -eq 0 ]; then
        log_message "SUCCESS" "Successfully executed $direction migration: $migration_name"
        record_migration "$migration_name" "$direction"
        return 0
    else
        log_message "ERROR" "Failed to execute $direction migration: $migration_name (Exit code: $exit_code)"
        return 1
    fi
}

record_migration() {
    local migration_name=$1
    local direction=$2
    local status="completed"
    if [ "$direction" = "down" ]; then
        status="rolled_back"
    fi
    
    local query="INSERT INTO migration_history (migration_name, status, executed_by) VALUES ('$migration_name', '$status', '$USER');"
    PGPASSWORD="$PGPASSWORD" psql -h "$PGHOST" -p "$PGPORT" -U "$PGUSER" -d "$PGDATABASE" -c "$query" > /dev/null 2>&1
}

case "$1" in
    up)
        if [ -z "$2" ]; then
            echo "Error: Migration name required."
            exit 1
        fi
        execute_migration "$2" "up"
        ;;
    down)
        if [ -z "$2" ]; then
            echo "Error: Migration name required."
            exit 1
        fi
        execute_migration "$2" "down"
        ;;
    *)
        echo "Usage: $0 {up|down} migration_name"
        exit 1
        ;;
esac
