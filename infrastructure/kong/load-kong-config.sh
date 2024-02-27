#!/bin/bash
KONG_ADMIN_URL=http://localhost:8001  # Change this if your Kong Admin API is on a different URL
CONFIG_FILE=./services.json  # Change this to the path of your Kong JSON config file

# Post the configuration to Kong's Admin API
curl -i -X POST "$KONG_ADMIN_URL/config" \
     -H "Content-Type: application/json" \
     -d @"$CONFIG_FILE"
