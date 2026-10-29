#!/bin/bash

source db_config.sh

VALIDATION_DIR="migrations/validation"
MIGRATION_NAME=$1

if [ -z "$MIGRATION_NAME" ]; then
    echo "Usage: $0 <migration_name>"
    exit 1
fi

VALIDATION_FILE="$VALIDATION_DIR/$MIGRATION_NAME.sql"

if [ ! -f "$VALIDATION_FILE" ]; then
    echo "Error: Validation script $VALIDATION_FILE not found."
    exit 1
fi

echo "=== Validation Suite for $MIGRATION_NAME ==="
PGPASSWORD="$PGPASSWORD" psql -h "$PGHOST" -p "$PGPORT" -U "$PGUSER" -d "$PGDATABASE" -f "$VALIDATION_FILE"
echo "=== Validation Complete ==="
