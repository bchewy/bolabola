# Auth service
This service is responsible for user authentication and authorization.

It will generate a JSON Web Token (JWT) for the user to use in the other services.

To power this service, we will be using Auth0. Auth0 is a flexible, drop-in solution to add authentication and authorization services to your applications. Your team and organization can avoid the cost, time, and risk that comes with building your own solution to authenticate and authorize users.

The reason we created a separate service for authentication is to make it easier to change the authentication method in the future. If we decide to change from Auth0 to another service, we can do so without affecting the other services.

Based off the JSON response from Auth0, we will use the id_token as the JWT.