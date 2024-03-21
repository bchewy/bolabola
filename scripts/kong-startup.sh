#!/bin/bash
# kong-startup.sh

# Wait for Kong to be ready
until curl --output /dev/null --silent --head --fail http://localhost:8001; do
    printf '.'
    sleep 5
done

# Import the Kong configuration
kong config db_import /etc/kong/kong.yml

# Keep the container running after the import
tail -f /dev/null

# Remember to give permission to the script using this command!
# chmod +x kong-startup.sh
