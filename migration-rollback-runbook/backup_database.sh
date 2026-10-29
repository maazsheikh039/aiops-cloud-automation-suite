#!/bin/bash

source db_config.sh

BACKUP_DIR="backups"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
BACKUP_FILE="${BACKUP_DIR}/inventory_db_${TIMESTAMP}.sql"

mkdir -p "$BACKUP_DIR"

create_backup() {
    echo "Creating backup at $BACKUP_FILE..."
    PGPASSWORD="$PGPASSWORD" pg_dump -h "$PGHOST" -p "$PGPORT" -U "$PGUSER" -d "$PGDATABASE" --format=plain --file="$BACKUP_FILE"
    if [ $? -eq 0 ]; then
        echo "Backup successfully created."
        return 0
    else
        echo "Backup failed!"
        return 1
    fi
}

validate_backup() {
    local backup_file=$1
    if [ -f "$backup_file" ] && [ -s "$backup_file" ]; then
        echo "Backup file validated: size > 0 bytes."
        return 0
    else
        echo "Backup validation failed: file is missing or empty."
        return 1
    fi
}

create_backup && validate_backup "$BACKUP_FILE"
