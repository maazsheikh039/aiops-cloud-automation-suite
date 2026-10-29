#!/bin/bash

source db_config.sh

restore_from_backup() {
    local backup_file=$1
    
    if [ ! -f "$backup_file" ]; then
        echo "Error: Backup file $backup_file not found."
        exit 1
    fi
    
    echo "Restoring database $PGDATABASE from $backup_file..."
    PGPASSWORD="$PGPASSWORD" psql -h "$PGHOST" -p "$PGPORT" -U "$PGUSER" -d "$PGDATABASE" -f "$backup_file"
    if [ $? -eq 0 ]; then
        echo "Database restored successfully."
    else
        echo "Restoration failed!"
        exit 1
    fi
}

if [ -z "$1" ]; then
    echo "Usage: $0 <backup_file>"
    exit 1
fi

restore_from_backup "$1"
