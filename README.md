<div align="center">
  <br>
  <h1>Authentication Flow 🖥️</h1>
  <strong>Complete User Authentication Flow</strong>
</div>
<br>

This file outlines the complete user authentication flow, focusing on the following APIs: user login, token generation, token refresh, and email verification via OTP. It also demonstrates the two-factor authentication (2FA) process, if enabled, and includes configurations for the forgot password API.

## Register API Flow

To register new user we have API with below context.

Endpoint: `POST /api/v1/auth/register/`

__Payload:__
```
{
  "email": "example@gmail.com",
  "password": "examplepassword"
}
```

__API Response__
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c",
  "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c"
}
```

__Note__: You can use the `access_token` as a `Bearer` token in the `Authorization` header.
The `refresh_token` can be used to generate a new `access_token` when the current one expires.

