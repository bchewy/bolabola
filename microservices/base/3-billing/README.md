 d# Billing Microservice
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
    "match_id": "1234",
    "match_name": "Arsenal vs Chelsea",
    "tickets": [
        {"category": "A", "quantity": 2},
        {"category": "B", "quantity": 3},
        {"category": "C", "quantity": 4},
        {"category": "Online", "quantity": 1}
    ],
    "user_id": "123"
    }'
```

## Concerns
- [:white_check_mark:] Stripe checkout, success, cancel links are using localhost. Any repurcussions?
- [:white_check_mark:] Test the stripe checkout page
- [:white_check_mark:] When checkout is successful, is the redirect to success page working?
- [ ] When checkout is successful, does it correctly update the db?