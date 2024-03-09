# User Profile Microservice
- main.py acts as the entry point for the user microservice.
- user_schemas is the pydantic models for the user_crud microservice and db.

The User Database will be in SQL and has 1 table:
- User Table

Sample User:
```
{
    "id": 1,
    "name": "John Doe",
    "email": "
    "stripe_id": "stripe_id",
    "username": "johndoe",
    "password": "password",
    "tickets": [
        {"match_id": 123, "ticket_category": "A", "serial_no": "1"},
        {"match_id": 456, "ticket_category": "A", "serial_no": "2"}
    ]
}
```

![user db schema](schema.png)
