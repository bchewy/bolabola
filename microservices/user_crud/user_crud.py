import os
import user_schemas
from datetime import datetime
from pydantic import BaseModel
from typing import Optional
import requests
from user_schemas import *

AUTH_ENDPOINT = os.environ.get('AUTH_ENDPOINT') # to create this endpoint in the future
STRIPE_ENDPOINT = os.environ.get('STRIPE_ENDPOINT') # to create this endpoint in the future

# get user from the database
def get_user(email: str) -> user_schemas.Account:
    """
    Get a user from the database
    """
    user_response = requests.get(f"{AUTH_ENDPOINT}/getUser/{email}")

    if user_response.status_code != 200:
        raise Exception("User not found")
    
    user_json = user_response.json()
    return user_schemas.UserAccount(
        id=user_json['id'],
        name=user_json['name'],
        email=user_json['email'],
        username=user_json['username'],
        created_at=datetime.strptime(user_json['created_at'], '%Y-%m-%d %H:%M:%S.%f'),
        updated_at=datetime.strptime(user_json['updated_at'], '%Y-%m-%d %H:%M:%S.%f')
    )
