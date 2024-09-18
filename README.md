<div align="center">
  <br>
  <h1>Authentication Flow 🖥️</h1>
  <strong>Complete User Authentication Flow</strong>
</div>
<br>

This file outlines the complete user authentication flow, focusing on the following APIs: user login, token generation, token refresh, and email verification via OTP. It also demonstrates the two-factor authentication (2FA) process, if enabled, and includes configurations for the forgot password API.


## Register API Flow 🚀

To register new user we have API with below context.

Endpoint: `POST /api/v1/auth/register/`

__Payload:__
```
{
  "username": "johnsmith",
  "email": "john@gmail.com",
  "password: "examplepassword",
  "firstName": "John",
  "lastName": "Smith",
  "DateOfBirth": "06-05-2002",
  "phone": "00000000000"
}
```

__API Response__

This API can have different responses based on the payload provided to it.

__Success User Registration__

__Response status code: 201__
```json
{
  "message": "User has been created"
}
```

__Note__: By default email is not verified, so you need to verify the email first
with `POST: /api/v1/auth/verify_email/` endpoint before signing and get access token.

__Validation Error__

__Response status code: 400__
```json
{
  "message": "Email already taken"
}
```
__Note__: This message can be change accordingly In case of validation
error i.e `username already taken, try another`, `phone already taken`.


## Login API Flow 🚀

To login to API, we need to verify the email first then we can get access token.

Endpoint: `POST /api/v1/auth/login/`

__Payload:__
```json
{
  "email": "example@gmail.com",
  "password": "ExamplePassword"
}
```

__API Response__

This API can have different responses based on verification on given data.

__Success Login__

__Response status code: 200__
```json
{
  "accessToken": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c",
  "refreshToken": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c"
}
```
__Validation Error__

__Response status code: 400__
```json
{
  "message": "Please verify your email first"
}
```

__Note__: In case of validation, the response message can be changed i.e. `Incorrect credentials`.

__In case of enabled 2FA__

If 2FA is enabled, the response will look like.

__Response status code: 200__
```json
{
  "message": "2FA required"
}
```

## Extra step in case of 2FA is enabled

You need to hit another endpoint (given below) after hitting the `POST /api/v1/auth/login/`.

Endpoint: `POST /api/v1/auth/login-2fa/`

__Payload:__
```json
{
  "totp": 123456,
}
```

__API Response__

This API can have different responses based on verification on given data.

__Success Login__

__Response status code: 200__
```json
{
  "accessToken": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c",
  "refreshToken": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c"
}
```

__Note__: You can use the `accessToken` value as a `Bearer` token in the `Authorization` header. The `refreshToken` can be used to generate a new `accesToken` when the current one expires.

__validation Error__

__Response status code: 400__
```json
{
  "message": "Incorrect TOTP"
}
```

__Note__: This TOTP is generated by the authenticator app i.e GoogleAuthenticator, the
flow of 2fA is described at end of document.


## Email Verification API Flow 🚀

To verify the email we have the below context.

Endpoint: `POST /api/v1/auth/send_code/`

__Payload:__
```
{
  "email": "john@gmail.com",
}
```

__API Response__

This API can have different responses based on the payload provided to it.

__Success__

__Response status code: 200__
```json
{
  "message": "A 6 digit code has been sent to your email"
}
```

__validation Error__

__Response status code: 400__
```json
{
  "message": "Incorrect email"
}
```

__Note__: In case of validation, the response message can be changed i.e. `Email is already verified, please login`.

## Verify code
Endpoint: `POST /api/v1/auth/verify_code/`

```json
{
  "code": 123456
}
```

__Success__

__Response status code: 200__
```json
{
  "message": "Congratulations! your email is verified."
}
```

__Validation Error__

__Response status code: 400__
```json
{
  "message": "Code expired"
}
```

__Note__: In case of validation, the response message can be changed i.e. `Incorrect code`.


## Fogot Password API Flow 🚀

To reset password, the following flow is available.

Endpoint: `POST /api/v1/auth/forgot_password/`

__Payload:__
```
{
  "email": "john@gmail.com"
}
```

__API Response__

This API can have different responses based on the payload provided to it.

__Success__

__Response status code: 200__
```json
{
  "message": "A 6 digit code has been sent to your respective email"
}
```

__Note__: In case of validation, the response message can be changed i.e. `Account does not exists`.


## Reset Password

Endpoint: `POST /api/v1/auth/reset_password/`

__Payload:__
```
{
  "email": "john@gmail.com",
  "code": 123456,
  "password": "12390@R0_",
  "confirmPassword": "12390@R0_"
}
```

__API Response__

This API can have different responses based on the payload provided to it.

__Success__

__Response status code: 200__
```json
{
  "message": "You password has been reset successfully!"
}
```

__Validation Error__

__Response status code: 400__
```json
{
  "message": "Incorrect code"
}
```

__Note__: In case of validation, the response message can be changed i.e. `Code Expired`, `Password does not match`.


## Enable 2FA and Login with 2FA 🚀

To enable 2FA authentication, the following flow is available.

Endpoint: `POST /api/v1/auth/enable-2fa/`

__Payload:__
```
{
  "email": "john@gmail.com",
  "password": "examplepassword",
}
```

__API Response__

This API can have different responses based on the payload provided to it.

__Success User Registration__

__Response status code: 201__
```json
{
  "qrCodeUrl": "https://example.com/qrcode?secret=ABC123",
  "manualKey": "ABC1234567890" // to manually enter in app i.e Google Authenticator
}
```

__validation Error__

__Response status code: 400__
```json
{
  "message": "Incorrect Password"
}
```

__Note__: The API can have different responses in case of validation. i.e. `Verify email before enabling 2FA`, 
`Incorrect account credentials`.

## Verify 2FA

Endpoint: `POST api/v1/auth/verify-2fa/`

__Payload:__
```
{
  "totp": 123456
}
```

__Success Enabling 2FA__

__Response status code: 200__
```json
{
  "message": "2FA has been enabled on this account!"
}
```

__Validation Error__

__Response status code: 400__
```json
{
  "message": "Incorrect totp"
}
```

__Note__: The API can have different responses in case of validation. i.e. `2FA process is not initiated`.
