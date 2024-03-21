#!/bin/bash

services=( "1-match" "2-queue" "3-billing" "4-user" "5-videoasset" "6-live-match" "7-notification" "8-logging" "9-seat")
username="bchewy"

for service in "${services[@]}"; do
  echo "Building $service"
  docker build -t $username/$service:latest ./microservices/base/$service
  echo "Pushing $service"
  docker push $username/$service:latest
done
