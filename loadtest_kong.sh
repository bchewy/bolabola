#!/bin/bash

# Set the base URL and route
base_url="http://localhost:8000"
route="/api/v1/match-streaming/65ec8436d73ef969919bdc86"

# Set the number of requests to make
num_requests=200

# Make the requests
for ((i=1; i<=num_requests; i++)); do
    echo "Request #$i"
    curl -X GET "$base_url$route"
    echo ""
    sleep 1  # Add a 1-second delay between requests
done