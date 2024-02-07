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
