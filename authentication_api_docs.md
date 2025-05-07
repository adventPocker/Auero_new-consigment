# Authentication API Documentation

## Overview
This document outlines the authentication endpoints for the Auero Backend API. The authentication system supports multiple user types including customers and vendors, with JWT token-based authentication.

## Base URL
```
/api/auth/
```

## Authentication
Most endpoints require JWT authentication. Include the JWT token in the Authorization header:
```
Authorization: Bearer <access_token>
```

## Endpoints

### 1. Customer Signup
Register a new customer account.

- **URL**: `/signup/customer/`
- **Method**: `POST`
- **Auth required**: No
- **Permissions**: None

#### Request Body
```json
{
    "username": "string",
    "email": "string",
    "password": "string",
    "user_type": "customer"
}
```

#### Success Response
```json
{
    "status": "success",
    "message": "Customer registration successful",
    "user": {
        "id": "integer",
        "username": "string",
        "email": "string",
        "user_type": "string"
    },
    "tokens": {
        "refresh": "string",
        "access": "string"
    }
}
```

### 2. Vendor Signup
Register a new vendor account.

- **URL**: `/signup/vendor/`
- **Method**: `POST`
- **Auth required**: No
- **Permissions**: None

#### Request Body
```json
{
    "username": "string",
    "email": "string",
    "password": "string",
    "phone_number": "string",
    "vendor_profile": {
        "vendor_type": "string",
        "company_name": "string",
        "contact_person": "string",
        "profile_image": "file"
    }
}
```

#### Success Response
```json
{
    "status": "success",
    "message": "Vendor registration successful",
    "user": {
        "id": "integer",
        "username": "string",
        "email": "string",
        "user_type": "vendor",
        "vendor_profile": {
            "vendor_type": "string",
            "company_name": "string",
            "contact_person": "string",
            "approved": "boolean"
        }
    },
    "tokens": {
        "refresh": "string",
        "access": "string"
    }
}
```

### 3. Login
Authenticate user and receive tokens.

- **URL**: `/login/`
- **Method**: `POST`
- **Auth required**: No
- **Permissions**: None

#### Request Body
```json
{
    "email": "string",
    "password": "string"
}
```

#### Success Response
```json
{
    "user": {
        "id": "integer",
        "username": "string",
        "email": "string",
        "user_type": "string"
    },
    "tokens": {
        "access": "string",
        "refresh": "string"
    }
}
```

### 4. Refresh Token
Get a new access token using refresh token.

- **URL**: `/refresh-token/`
- **Method**: `POST`
- **Auth required**: No
- **Permissions**: None

#### Request Body
```json
{
    "refresh": "string"
}
```

#### Success Response
```json
{
    "access": "string"
}
```

### 5. Logout
Blacklist the refresh token.

- **URL**: `/logout/`
- **Method**: `POST`
- **Auth required**: No
- **Permissions**: None

#### Request Body
```json
{
    "refresh_token": "string"
}
```

#### Success Response
```json
{
    "status": "success",
    "message": "Successfully logged out"
}
```

### 6. Current User Info
Get information about the currently authenticated user.

- **URL**: `/me/`
- **Method**: `GET`
- **Auth required**: Yes
- **Permissions**: IsAuthenticated

#### Success Response for Customer
```json
{
    "status": "success",
    "user": {
        "id": "integer",
        "username": "string",
        "email": "string",
        "user_type": "customer"
    }
}
```

#### Success Response for Vendor
```json
{
    "status": "success",
    "user": {
        "id": "integer",
        "username": "string",
        "email": "string",
        "user_type": "vendor",
        "vendor_profile": {
            "vendor_type": "string",
            "company_name": "string",
            "contact_person": "string",
            "approved": "boolean",
            "profile_image": "string (URL)"
        }
    }
}
```

### 7. Address Management

#### 7.1 List/Create Address
Get all addresses or create a new address for the authenticated user.

- **URL**: `/addresses/`
- **Method**: `GET`, `POST`
- **Auth required**: Yes
- **Permissions**: IsAuthenticated

##### POST Request Body
```json
{
    "address_line1": "string",
    "address_line2": "string",
    "city": "string",
    "state": "string",
    "postal_code": "string",
    "country": "string"
}
```

##### GET Success Response
```json
[
    {
        "address_line1": "string",
        "address_line2": "string",
        "city": "string",
        "state": "string",
        "postal_code": "string",
        "country": "string"
    }
]
```

#### 7.2 Retrieve/Update/Delete Address
Manage specific address by ID.

- **URL**: `/addresses/{id}/`
- **Method**: `GET`, `PUT`, `DELETE`
- **Auth required**: Yes
- **Permissions**: IsAuthenticated

##### PUT Request Body
```json
{
    "address_line1": "string",
    "address_line2": "string",
    "city": "string",
    "state": "string",
    "postal_code": "string",
    "country": "string"
}
```

## Error Responses

### 400 Bad Request
```json
{
    "status": "error",
    "message": "Invalid data provided",
    "errors": {
        "field": ["error details"]
    }
}
```

### 401 Unauthorized
```json
{
    "status": "error",
    "message": "Invalid credentials"
}
```

### 403 Forbidden
```json
{
    "detail": "You do not have permission to perform this action."
}
```

### 500 Internal Server Error
```json
{
    "status": "error",
    "message": "An unexpected error occurred"
}
```

## Notes
- All timestamps are returned in ISO 8601 format
- File uploads should be sent as `multipart/form-data`
- Token expiry times:
  - Access Token: 5 minutes
  - Refresh Token: 24 hours 