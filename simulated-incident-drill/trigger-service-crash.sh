#!/bin/bash
# Simulates service failure by stopping Nginx and introducing a syntax error

echo "Triggering service crash incident..."
sudo systemctl stop nginx

# Introduce deliberate syntax error in Nginx config to prevent restart
sudo sed -i 's/listen 8080;/listen 8080 invalid_directive;/g' /etc/nginx/sites-available/incident-app

echo "Service crash incident triggered"
