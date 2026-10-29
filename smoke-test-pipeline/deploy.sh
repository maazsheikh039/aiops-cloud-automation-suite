#!/bin/bash

echo "Starting deployment..."

# Stop existing application
pkill -f "node app/server.js" 2>/dev/null || true
sleep 2

# Start application in background
cd ~/smoke-test-lab
nohup node app/server.js > app.log 2>&1 &

# Wait for application to start
sleep 3

echo "Deployment completed"
echo "Application PID: $(pgrep -f 'node app/server.js')"
