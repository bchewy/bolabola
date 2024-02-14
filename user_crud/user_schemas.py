from datetime import datetime
from pydantic import BaseModel
from typing import Optional

# how pydantic works
# https://pydantic-docs.helpmanual.io/usage/models/

# simply put, UserCredentialsBase is a class that inherits from BaseModel,
# and UserCredentialsCreate is a class that inherits from UserCredentialsBase.

class UserCredentialsBase(BaseModel):
    password: str

class UserCredentialsCreate(UserCredentialsBase):
    name: str
    email: str
    username: str

class UserLogin(UserCredentialsBase):
    username: str

class UserAccountBase(BaseModel):
    id: int
    name: str
    email: str
    username: str
    stripe_id: str
    created_at: datetime
    updated_at: datetime

class UserAccountCreate(UserAccountBase):
    password: str

class UserAccount(UserAccountBase):
    pass
