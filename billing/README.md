# Billing Microservice
This microservice is responsible for billing and payment processing. It is a RESTful API that provides the following endpoint:

`POST /checkout`
Called by user when the frontend checkout button is clicked. This endpoint creates a new order and returns the order id.
---
## Setup:
Create a post request to /checkout. 
The server returns a redirect to a Stripe subscription checkout page. 
Enter testing payment details (card number 4242 4242 4242 4242) with any email and an expiry date in the future. 
User will then be redirected to the success page.

## to test:
```zsh
curl -X POST http://localhost:5000/checkout \
     -H "Content-Type: application/json" \
     -d '{
    "order_id": "1234",
    "show_name": "Hamilton",
    "show_datetime": "2024-02-10T19:00:00",
    "tickets": [
        {"category": "A", "price": 400, "quantity": 2},
        {"category": "B", "price": 300, "quantity": 3},
        {"category": "C", "price": 200, "quantity": 4}
    ],
    "total": 2600,
    "user_id": "123"
    }'
```