#!/bin/bash
cd "$(dirname "$0")"
source venv/bin/activate

mkdir -p logs

# Start API server in background
python3 api/automation_api.py > logs/api.log 2>&1 &
API_PID=$!
echo "API started with PID: $API_PID"

# Start Celery worker in background
celery -A workers.task_worker worker --loglevel=info > logs/celery.log 2>&1 &
WORKER_PID=$!
echo "Worker started with PID: $WORKER_PID"

echo "Platform started successfully!"
echo "To stop later, run: kill $API_PID $WORKER_PID"
