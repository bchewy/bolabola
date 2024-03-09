#!/bin/bash
# Wait for MongoDB to be ready
# until mongo --host mongodb-service-name --eval "print(\"waited for connection\")"; do
#   >&2 echo "MongoDB is unavailable - sleeping"
#   sleep 1
# done

# Run mongoimport
mongoimport --host mongodb --db matches --collection matches --type json --file /app/init.json --jsonArray

# Keep container running if needed
# tail -f /dev/null
