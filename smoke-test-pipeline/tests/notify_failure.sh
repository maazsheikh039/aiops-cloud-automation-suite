#!/bin/bash

REPORT_FILE="$1"
NOTIFICATION_LOG="reports/notifications.log"

send_notification() {
    local status="$1"
    local report_content="$2"
    
    echo "$(date): Deployment $status" >> "$NOTIFICATION_LOG"
    echo "$report_content" >> "$NOTIFICATION_LOG"
    echo "---" >> "$NOTIFICATION_LOG"
}

if [ -f "$REPORT_FILE" ]; then
    if grep -q "FAILED" "$REPORT_FILE"; then
        send_notification "FAILED" "$(cat $REPORT_FILE)"
        echo "Failure notification sent"
    else
        send_notification "PASSED" "$(cat $REPORT_FILE)"
        echo "Success notification sent"
    fi
fi
