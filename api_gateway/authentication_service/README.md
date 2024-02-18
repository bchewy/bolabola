# Auth service
This service is responsible for user authentication and authorization.

It will generate a JSON Web Token (JWT) for the user to use in the other services.

To power this service, we will be using Auth0. Auth0 is a flexible, drop-in solution to add authentication and authorization services to your applications. Your team and organization can avoid the cost, time, and risk that comes with building your own solution to authenticate and authorize users.

The reason we created a separate service for authentication is to make it easier to change the authentication method in the future. If we decide to change from Auth0 to another service, we can do so without affecting the other services.

Based off the JSON response from Auth0, we will use the id_token as the JWT.

# sample response from Auth0
```json
{
    "access_token": "abc",
    "expires_at": 1708353710,
    "expires_in": 86400,
    "id_token": "abcd",
    "scope": "openid profile email",
    "token_type": "Bearer",
    "userinfo": {
        "aud": "87CiuJFZSPboq2IkQTLT5QDIZeyXtKyK",
        "email": "test@gmail.com",
        "email_verified": true,
        "exp": abcd,
        "given_name": "yiji",
        "iat": test,
        "iss": "https://dev-test.us.auth0.com/",
        "locale": "en",
        "name": "test",
        "nickname": "test",
        "nonce": "abcd",
        "picture": "",
        "sid": "abcd",
        "sub": "abcd",
        "updated_at": "2024-02-18T14:41:49.274Z"
    }
}
```