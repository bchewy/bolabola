# Refund Orchestrator Microservice
- refund.py acts as the entry point for the refund orchestrator microservice.

General flow of the refund orchestrator microservice:
1. receives ticket information from frontend
2. calls billing service for refund
3. receives a status from billing service, success/failure
4. if success, send ticket information to RabbitMQ to update db

YET TO IMPLEMENT:
- Set up the message to be sent
- Send the message
