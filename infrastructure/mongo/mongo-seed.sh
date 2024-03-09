#!/bin/bash
echo "Waiting for MongoDB to start..."
# Wait for MongoDB to start
sleep 10 # Adjust sleep as necessary

echo "MongoDB started."

pip install pymongo Faker
# Run Python seed script
python seed.py
