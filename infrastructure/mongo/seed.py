from faker import Faker
from pymongo import MongoClient
from datetime import datetime
import random

# Initialize Faker
fake = Faker()

# Connect to MongoDB (adjust the URI as necessary)
client = MongoClient('mongodb://localhost:27017/')

# create a mongo database for me
db = client['matchs_db']
collection = db['matches']  # Use your collection name

# Function to create fake match data
def create_fake_match():
    return {
        "name": fake.sentence(nb_words=6),
        "description": fake.text(),
        "date": fake.date_time_between(start_date='-1y', end_date='now').strftime('%Y-%m-%d %H:%M:%S'),
        "venue": fake.city(),
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow(),
    }

# Insert fake match data
for _ in range(10):  # Adjust the number for how many entries you want
    new_event = create_fake_match()
    collection.insert_one(new_event)

print("Fake match data inserted.")
