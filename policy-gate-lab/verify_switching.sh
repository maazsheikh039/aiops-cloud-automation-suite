#!/bin/bash

echo "Testing dynamic profile switching and enforcement..."

echo "1. Listing available profiles:"
curl -s http://localhost:8080/profiles | jq '.'

for profile in healthcare finance retail; do
    echo -n "Switching to $profile profile: "
    curl -s -X POST http://localhost:8080/switch-profile \
      -H "Content-Type: application/json" \
      -d "{\"profile\": \"$profile\"}" | jq -c '.'
      
    echo -n "Active status: "
    curl -s http://localhost:8080/status | jq -c '.'
    echo ""
done
