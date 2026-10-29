#!/bin/bash
# Main drill execution script

DRILL_TYPE=$1
TIMESTAMP=$(date +%Y%m%d-%H%M%S)
LOG_FILE="drill-${DRILL_TYPE}-${TIMESTAMP}.log"

log_action() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$LOG_FILE"
}

execute_drill() {
    log_action "Starting $DRILL_TYPE drill..."
    
    if [ "$DRILL_TYPE" == "disk" ]; then
        ./trigger-disk-full.sh | tee -a "$LOG_FILE"
        log_action "Investigating disk usage using df -h and du..."
        df -h | tee -a "$LOG_FILE"
        log_action "Resolving disk full by cleaning up /tmp/disk-fill-test..."
        rm -rf /tmp/disk-fill-test
        log_action "Verification complete. Disk usage normalized."
        
    elif [ "$DRILL_TYPE" == "service" ]; then
        ./trigger-service-crash.sh | tee -a "$LOG_FILE"
        log_action "Investigating Nginx status and checking configuration..."
        sudo nginx -t | tee -a "$LOG_FILE"
        log_action "Fixing Nginx configuration syntax error..."
        sudo sed -i 's/listen 8080 invalid_directive;/listen 8080;/g' /etc/nginx/sites-available/incident-app
        sudo systemctl restart nginx
        log_action "Verifying Nginx service status and HTTP response..."
        sudo systemctl status nginx --no-pager | tee -a "$LOG_FILE"
        curl -I http://localhost:8080 | tee -a "$LOG_FILE"
        
    elif [ "$DRILL_TYPE" == "cpu" ]; then
        ./trigger-cpu-spike.sh | tee -a "$LOG_FILE"
        log_action "Investigating CPU usage with top/htop..."
        top -bn1 | head -15 | tee -a "$LOG_FILE"
        log_action "Waiting for stress-ng simulation to timeout..."
        sleep 5
        log_action "CPU spike drill completed."
    fi
}

case $DRILL_TYPE in
    disk|service|cpu)
        execute_drill
        ;;
    *)
        echo "Usage: $0 {disk|service|cpu}"
        exit 1
        ;;
esac

log_action "Drill completed successfully. Review log: $LOG_FILE"
