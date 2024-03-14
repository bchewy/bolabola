#!/bin/bash
# Wait for MongoDB to be ready
# until mongo --host mongodb-service-name --eval "print(\"waited for connection\")"; do
#   >&2 echo "MongoDB is unavailable - sleeping"
#   sleep 1
# done

# Run mongoimport, if matches db is empty; 
# Currently the code here does not work due to the fact that.... mongo command is not found in the container!! - so dumb.. it's a mongo image..
# mongo matches --eval "db.matches.count()" --quiet | grep 0
# if [ $? -eq 0 ]; then
#   echo "Database is empty. Seeding data..."
#   mongoimport --host mongodb --db matches --collection matches --type json --file /app/init.json --jsonArray
# else
#   echo "Database is not empty. Skipping seeding..."
# fi
mongoimport --host mongodb --db matches --collection matches --type json --file /app/init.json --jsonArray

# Keep container running if needed
tail -f /dev/null
