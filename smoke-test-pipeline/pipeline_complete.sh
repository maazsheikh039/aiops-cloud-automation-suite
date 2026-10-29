#!/bin/bash

set -e

PIPELINE_LOG="reports/pipeline_$(date +%Y%m%d_%H%M%S).log"
mkdir -p reports

log_pipeline() {
    echo "[$(date +%H:%M:%S)] $1" | tee -a "$PIPELINE_LOG"
}

pre_deployment_checks() {
    log_pipeline "=== Pre-Deployment Checks ==="
    if lsof -i:3000 >/dev/null 2>&1; then
        log_pipeline "Port 3000 is in use, stopping existing process"
        pkill -f "node app/server.js" || true
        sleep 2
    fi
    
    if [ ! -f "app/server.js" ]; then
        log_pipeline "ERROR: Application file not found"
        exit 1
    fi
    log_pipeline "Pre-deployment checks passed"
}

deploy_application() {
    log_pipeline "=== Deploying Application ==="
    ./deploy.sh >> "$PIPELINE_LOG" 2>&1
    sleep 5
    
    if pgrep -f "node app/server.js" > /dev/null; then
        log_pipeline "Application deployed successfully"
    else
        log_pipeline "ERROR: Application failed to start"
        exit 1
    fi
}

run_smoke_tests() {
    log_pipeline "=== Running Smoke Tests ==="
    ./tests/smoke_tests_complete.sh
    return $?
}

handle_results() {
    local test_result=$1
    log_pipeline "=== Processing Results ==="
    
    latest_report=$(ls -t reports/smoke_test_report_*.txt 2>/dev/null | head -n1)
    if [ -n "$latest_report" ]; then
        ./tests/notify_failure.sh "$latest_report"
    fi
    
    if [ $test_result -ne 0 ]; then
        log_pipeline "ALERT: Smoke tests failed - consider rollback"
        return 1
    fi
    return 0
}

log_pipeline "Starting deployment pipeline"
pre_deployment_checks
deploy_application
run_smoke_tests
test_exit_code=$?
handle_results $test_exit_code

if [ $test_exit_code -eq 0 ]; then
    log_pipeline "Pipeline completed successfully"
    exit 0
else
    log_pipeline "Pipeline failed - review reports"
    exit 1
fi
