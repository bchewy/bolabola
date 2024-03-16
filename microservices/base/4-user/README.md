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
    "email": "john@example.com"
    "stripe_id": "123",
    "username": "johndoe",
    "password": "johndoe",
    "tickets": [
        {"match_id": 123, "ticket_category": "A", "serial_no": "1", "charge_id": "abc"},
        {"match_id": 456, "ticket_category": "A", "serial_no": "2"}, "charge_id": "cbd",
    ]
}
```
note that stripe_id is optional and is only present if the user has bought a ticket.

![user db schema](schema.png)


If you get this error in mysql:
`--initialize specified but the data directory has files in it. Aborting...`
Delete the `dbdata` folder and compose up again.

## Issues
- [ ] RabbitMQ is not working