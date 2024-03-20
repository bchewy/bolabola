#!/bin/bash
mongoimport --host mongodb --db matches --collection matches --type json --file /app/init.json --jsonArray
mongoimport --host mongodb --db tickets --collection tickets --type json --file /app/init-ticket.json --jsonArray
tail -f /dev/null
