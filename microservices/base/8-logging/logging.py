import logging
from pymongo import MongoClient

# localhost is mongodb here because mongodb is our service name in the docker-compose file
client = MongoClient('mongodb://mongodb:27017/')
db = client['logs']
collection = db['log_entries']

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def log_entry(message):
    # Log the message
    logging.info(message)
    
    # Store the log entry in MongoDB
    collection.insert_one({'message': message})