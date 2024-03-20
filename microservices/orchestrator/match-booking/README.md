# Match booking orchestrator

**Scenario 1: User buys a ticket for a match**
When user clicks on proceed to checkout button,
1) call the "/init-match-booking" endpoint
    - It calls the seat reservation microservice to reserve the seats (`reserve_seat_for_user` function)
    - When reservation is successful, executes `continute_match_booking` function
        - The `continue_match_booking` function makes a call to billing microservice to create a checkout session for the user
2) When the user succesfully makes a payment on the Stripe checkout page, "process_webhook" endpoint will be called
    - Send the match booking details to RabbitMQ

    