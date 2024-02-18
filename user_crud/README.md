
- main.py acts as the entry point for the user microservice.
- user_crud is the logic for crud on the users, including auth.
- user_schemas is the pydantic models for the user_crud microservice and db.

yet to implement
1. set endpoint for authentication and change the code. RN it just checks if the user name is in the db -> make sure that it returns a json that user_crud is ok with receiving
    authentication is for the gateway, so we need it to be done correctly

do i need to get token ah? or just check if the user is in the db? i think just check if the user is in the db. if the user is in the db, then the user is authenticated. if the user is not in the db, then the user is not authenticated. 
