# Mobile App API Documentation

This document provides details for the backend API endpoints relevant to the mobile application development.

**Base URL**: The base URL for all API endpoints will be provided separately (e.g., `https://api.example.com/api/`). All endpoint paths below are relative to this base URL.

**Authentication**:
*   Most user-specific endpoints require authentication using a JWT token.
*   The token should be included in the `Authorization` header of the request: `Authorization: Bearer <your_access_token>`.
*   Endpoints marked with `Authentication Required: Yes` need this header. Endpoints marked `Authentication Required: No` are public.

---

## 1. Authentication (`/auth/`)

### 1.1. Customer Registration

*   **Endpoint**: `POST /auth/signup/customer/`
*   **Description**: Registers a new customer account.
*   **Authentication Required**: No
*   **Request Body**:
    ```json
    {
        "username": "customer_username",
        "email": "customer@example.com",
        "password": "securepassword123",
        "user_type": "customer" // Should be 'customer'
    }
    ```
*   **Response (Success - 201 Created)**:
    ```json
    {
        "status": "success",
        "message": "Customer registration successful",
        "user": {
            "id": 1,
            "username": "customer_username",
            "email": "customer@example.com",
            "user_type": "customer",
            "phone_number": null,
            "profile_image": null
        },
        "tokens": {
            "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
            "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
        }
    }
    ```
*   **Response (Error - 400 Bad Request)**:
    ```json
    {
        "status": "error",
        "message": "Invalid data provided",
        "errors": {
            "email": ["Enter a valid email address."]
        }
    }
    ```

### 1.2. User Login

*   **Endpoint**: `POST /auth/login/`
*   **Description**: Logs in an existing user (customer or vendor) and returns access/refresh tokens.
*   **Authentication Required**: No
*   **Request Body**:
    ```json
    {
        "email": "user@example.com", // Can also use 'username'
        "password": "userpassword"
    }
    ```
*   **Response (Success - 200 OK)**:
    ```json
    {
        "user": {
            "id": 1,
            "username": "testuser",
            "email": "user@example.com",
            "user_type": "customer", // or "vendor"
            "phone_number": null,
            "profile_image": null
        },
        "tokens": {
            "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
            "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
        }
    }
    ```
*   **Response (Error - 401 Unauthorized)**:
    ```json
    {
        "status": "error",
        "message": "Invalid credentials"
    }
    ```

### 1.3. Refresh Access Token

*   **Endpoint**: `POST /auth/refresh-token/`
*   **Description**: Obtains a new access token using a valid refresh token.
*   **Authentication Required**: No
*   **Request Body**:
    ```json
    {
        "refresh": "your_refresh_token"
    }
    ```
*   **Response (Success - 200 OK)**:
    ```json
    {
        "access": "new_access_token"
    }
    ```
*   **Response (Error - 401 Unauthorized)**:
    ```json
    {
        "detail": "Token is invalid or expired",
        "code": "token_not_valid"
    }
    ```

### 1.4. Logout

*   **Endpoint**: `POST /auth/logout/`
*   **Description**: Blacklists the provided refresh token to log the user out.
*   **Authentication Required**: No (but typically called by an authenticated user)
*   **Request Body**:
    ```json
    {
        "refresh_token": "your_refresh_token"
    }
    ```
*   **Response (Success - 200 OK)**:
    ```json
    {
        "message": "Logout successful"
    }
    ```
*   **Response (Error - 400 Bad Request)**:
    ```json
    {
        "error": "Refresh token is required"
    }
    ```

### 1.5. Get Current User Details

*   **Endpoint**: `GET /auth/me/`
*   **Description**: Retrieves the profile information of the currently authenticated user.
*   **Authentication Required**: Yes
*   **Response (Success - 200 OK)**:
    ```json
    {
        "user": {
            "id": 1,
            "username": "currentuser",
            "email": "currentuser@example.com",
            "user_type": "customer",
            "phone_number": "1234567890",
            "profile_image": "/media/profile_images/image.jpg" // URL or null
        }
    }
    ```

### 1.6. Update Current User Details

*   **Endpoint**: `PATCH /auth/me/`
*   **Description**: Updates the profile information of the currently authenticated user.
*   **Authentication Required**: Yes
*   **Request Body** (include only fields to be updated):
    ```json
    {
        "username": "newusername",
        "email": "newemail@example.com",
        "phone_number": "0987654321",
        "profile_image": null // To remove image, or provide a new file upload for image update (multipart/form-data)
    }
    ```
    *Note: If sending `profile_image` as a file, use `multipart/form-data` content type.*
*   **Response (Success - 200 OK)**:
    ```json
    {
        "status": "success",
        "message": "Profile updated successfully",
        "user": {
            "id": 1,
            "username": "newusername",
            "email": "newemail@example.com",
            "user_type": "customer",
            "phone_number": "0987654321",
            "profile_image": null
        }
    }
    ```

### 1.7. Change Password

*   **Endpoint**: `POST /auth/password/change/`
*   **Description**: Allows an authenticated user to change their password.
*   **Authentication Required**: Yes
*   **Request Body**:
    ```json
    {
        "old_password": "current_password",
        "new_password": "brand_new_strong_password"
    }
    ```
*   **Response (Success - 200 OK)**:
    ```json
    {
        "status": "success",
        "message": "Password changed successfully"
    }
    ```
*   **Response (Error - 400 Bad Request)**:
    ```json
    {
        "status": "error",
        "message": "Old password is not correct" // or other validation errors
    }
    ```

### 1.8. Request Password Reset

*   **Endpoint**: `POST /auth/password/reset/`
*   **Description**: Initiates the password reset process for a user by sending a reset token/link (actual email sending mechanism is backend-dependent and not detailed here).
*   **Authentication Required**: No
*   **Request Body**:
    ```json
    {
        "email": "user_email@example.com"
    }
    ```
*   **Response (Success - 200 OK)**:
    ```json
    {
        "status": "success",
        "message": "Password reset email sent." // Message might vary based on backend implementation
    }
    ```
*   **Response (Error - 404 Not Found)**:
    ```json
    {
        "status": "error",
        "message": "User with this email not found."
    }
    ```

### 1.9. Confirm Password Reset

*   **Endpoint**: `POST /auth/password/reset/confirm/`
*   **Description**: Sets a new password using the token received from the password reset request.
*   **Authentication Required**: No
*   **Request Body**:
    ```json
    {
        "uidb64": "base64_encoded_user_id", // Provided in the reset link/email
        "token": "password_reset_token",     // Provided in the reset link/email
        "new_password": "new_secure_password"
    }
    ```
*   **Response (Success - 200 OK)**:
    ```json
    {
        "status": "success",
        "message": "Password has been reset successfully."
    }
    ```
*   **Response (Error - 400 Bad Request)**:
    ```json
    {
        "status": "error",
        "message": "Invalid token or user ID." // or password validation errors
    }
    ```

### 1.10. Manage Addresses

#### 1.10.1. List Addresses

*   **Endpoint**: `GET /auth/addresses/`
*   **Description**: Retrieves a list of addresses for the authenticated user.
*   **Authentication Required**: Yes
*   **Response (Success - 200 OK)**:
    ```json
    [
        {
            "address_line1": "123 Main St",
            "address_line2": "Apt 4B",
            "city": "Anytown",
            "state": "CA",
            "postal_code": "90210",
            "country": "USA"
        },
        // ... more addresses
    ]
    ```

#### 1.10.2. Create Address

*   **Endpoint**: `POST /auth/addresses/`
*   **Description**: Adds a new address for the authenticated user.
*   **Authentication Required**: Yes
*   **Request Body**:
    ```json
    {
        "address_line1": "456 Oak Ave",
        "address_line2": "",
        "city": "Otherville",
        "state": "NY",
        "postal_code": "10001",
        "country": "USA"
    }
    ```
*   **Response (Success - 201 Created)**: (Returns the created address object)
    ```json
    {
        "address_line1": "456 Oak Ave",
        "address_line2": "",
        "city": "Otherville",
        "state": "NY",
        "postal_code": "10001",
        "country": "USA"
    }
    ```

#### 1.10.3. Retrieve/Update/Delete Address

*   **Endpoint**: `GET /auth/addresses/<int:pk>/`
*   **Endpoint**: `PUT /auth/addresses/<int:pk>/`
*   **Endpoint**: `PATCH /auth/addresses/<int:pk>/`
*   **Endpoint**: `DELETE /auth/addresses/<int:pk>/`
*   **Description**:
    *   `GET`: Retrieves a specific address.
    *   `PUT`: Updates a specific address (all fields required).
    *   `PATCH`: Partially updates a specific address (only fields to change).
    *   `DELETE`: Deletes a specific address.
*   **Authentication Required**: Yes
*   **URL Parameter**: `pk` - The ID of the address.
*   **Request Body (for PUT/PATCH)**:
    ```json
    {
        "address_line1": "789 Pine Ln",
        // ... other fields
    }
    ```
*   **Response (Success)**:
    *   `GET, PUT, PATCH`: 200 OK (Returns the address object)
    *   `DELETE`: 204 No Content
*   **Response (Error - 404 Not Found)**: If address with `pk` does not exist or does not belong to the user.

---

## 2. Products & Categories (`/products/`)

### 2.1. List Categories

*   **Endpoint**: `GET /products/categories/`
*   **Description**: Retrieves a list of all product categories.
*   **Authentication Required**: No (Typically public, but can be restricted)
*   **Response (Success - 200 OK)**:
    ```json
    [
        {
            "id": 1,
            "name": "Electronics",
            "name_ar": "إلكترونيات",
            "slug": "electronics",
            "description": "All kinds of electronic gadgets.",
            "description_ar": "جميع أنواع الأجهزة الإلكترونية.",
            "banner_image": "/media/category_banners/electronics.jpg",
            "image": "/media/category_images/electronics_thumb.jpg",
            "parent": null, // ID of parent category or null
            "is_active": true,
            "created_at": "2023-01-01T12:00:00Z",
            "updated_at": "2023-01-01T12:00:00Z"
        },
        // ... more categories
    ]
    ```

### 2.2. Get Category Details

*   **Endpoint**: `GET /products/categories/<int:pk>/`
*   **Description**: Retrieves details of a specific category.
*   **Authentication Required**: No
*   **URL Parameter**: `pk` - The ID of the category.
*   **Response (Success - 200 OK)**: (Single category object, same structure as in List Categories)

### 2.3. List Products in a Category

*   **Endpoint**: `GET /products/categories/<int:pk>/products/`
*   **Description**: Retrieves a list of products belonging to a specific category. Supports pagination.
*   **Authentication Required**: No
*   **URL Parameter**: `pk` - The ID of the category.
*   **Query Parameters (Optional)**:
    *   `page`: Page number for pagination.
    *   `page_size`: Number of items per page.
*   **Response (Success - 200 OK)**:
    ```json
    {
        "count": 150,
        "next": "https://api.example.com/api/products/categories/1/products/?page=2",
        "previous": null,
        "results": [
            {
                "id": 101,
                "vendor": 5, // Vendor User ID
                "vendor_name": "Luxury Goods Inc.",
                "category": 1, // Category ID
                "category_name": "Electronics",
                "name": "Smartphone X",
                "name_ar": "هاتف ذكي إكس",
                "slug": "smartphone-x",
                "description": "Latest model smartphone.",
                "description_ar": "أحدث موديل للهواتف الذكية.",
                "vendor_price": "600.00", // Price vendor wants
                "selling_price": "699.99", // Price set by admin/platform
                "platform_fee": "69.99",
                "vendor_payout": "630.00",
                "payout_status": "PENDING", // PENDING or PAID
                "status": "APPROVED", // DRAFT, SUBMITTED, INSPECTION, APPROVED, REJECTED, SOLD
                "inspection_notes": "Looks good.",
                "created_at": "2023-02-10T10:00:00Z",
                "updated_at": "2023-02-11T15:30:00Z",
                "images": [
                    {
                        "id": 1,
                        "image": "/media/product_images/phone_front.jpg",
                        "is_primary": true,
                        "created_at": "2023-02-10T10:05:00Z"
                    },
                    // ... more images
                ],
                "consignment": { // Consignment details, structure might vary
                    "id": 1,
                    "handover_date": "2023-02-09T14:00:00Z",
                    "inspection_date": "2023-02-11T10:00:00Z",
                    "physical_status": "INSPECTED",
                    "inspector": 2, // Admin User ID
                    "inspector_name": "Admin Inspector",
                    "quality_notes": "Excellent condition.",
                    "authentication_notes": "Verified authentic.",
                    "created_at": "2023-02-09T14:00:00Z",
                    "updated_at": "2023-02-11T10:00:00Z"
                }
            },
            // ... more products
        ]
    }
    ```
    *Note: The pagination structure (`count`, `next`, `previous`, `results`) is common for paginated list views.*

### 2.4. List All Products (General Listing/Search)

*   **Endpoint**: `GET /products/products/`
*   **Description**: Retrieves a list of all products, often used for a general product listing page. Supports pagination and potentially filtering/sorting if implemented by the backend (not detailed here beyond basic pagination). For customer view, this should ideally only show 'APPROVED' products.
*   **Authentication Required**: No (for viewing approved products)
*   **Query Parameters (Optional)**:
    *   `page`: Page number.
    *   `page_size`: Items per page.
    *   `search`: Search term (e.g., `?search=laptop`)
    *   `category`: Category ID to filter by (e.g., `?category=1`)
    *   `min_price`, `max_price`: Price range filtering.
    *   `ordering`: Field to sort by (e.g., `?ordering=selling_price` or `?ordering=-selling_price` for descending).
*   **Response (Success - 200 OK)**: (Paginated list of product objects, same structure as in 2.3)

### 2.5. Get Product Details

*   **Endpoint**: `GET /products/products/<int:pk>/`
*   **Description**: Retrieves details of a specific product.
*   **Authentication Required**: No (for viewing approved products)
*   **URL Parameter**: `pk` - The ID of the product.
*   **Response (Success - 200 OK)**: (Single product object, same structure as in 2.3)

### 2.6. Search Products

*   **Endpoint**: `GET /products/search/`
*   **Description**: Provides a dedicated endpoint for searching products based on various criteria.
*   **Authentication Required**: No
*   **Query Parameters (Example)**:
    *   `query`: The search term (e.g., `?query=luxury watch`)
    *   `category`: Category name or ID (e.g., `?category=Watches` or `?category=3`)
    *   `min_price`: Minimum selling price (e.g., `?min_price=500`)
    *   `max_price`: Maximum selling price (e.g., `?max_price=2000`)
    *   `status`: Product status (e.g., `?status=APPROVED`) - Important for customer-facing search.
    *   `ordering`: Sort order (e.g., `?ordering=name` or `?ordering=-created_at`)
    *   `page`, `page_size`: For pagination.
*   **Response (Success - 200 OK)**: (Paginated list of product objects, same structure as in 2.3)

---

## 3. Cart (`/cart/`)

### 3.1. User Cart Operations (Authenticated Users)

#### 3.1.1. Get User Cart

*   **Endpoint**: `GET /cart/user/`
*   **Description**: Retrieves the cart for the authenticated user.
*   **Authentication Required**: Yes
*   **Response (Success - 200 OK)**:
    ```json
    {
        "id": 1,
        "user": 15, // User ID
        "items": [
            {
                "id": 10, // CartItem ID
                "product": { /* Full Product Serializer data as in 2.3 */ },
                "product_id": 101, // Product ID (write-only for add/update)
                "quantity": 2,
                "added_at": "2023-03-01T10:00:00Z"
            },
            // ... more items
        ],
        "created_at": "2023-03-01T09:00:00Z",
        "updated_at": "2023-03-01T10:00:00Z"
    }
    ```

#### 3.1.2. Add Item to User Cart

*   **Endpoint**: `POST /cart/user/add/`
*   **Description**: Adds a product to the authenticated user's cart or updates quantity if already present.
*   **Authentication Required**: Yes
*   **Request Body**:
    ```json
    {
        "product_id": 101,
        "quantity": 1 // Optional, defaults to 1
    }
    ```
*   **Response (Success - 200 OK)**: (Full cart data as in 3.1.1)

#### 3.1.3. Remove Item from User Cart

*   **Endpoint**: `POST /cart/user/remove/`
*   **Description**: Removes a product entirely from the authenticated user's cart.
*   **Authentication Required**: Yes
*   **Request Body**:
    ```json
    {
        "product_id": 101
    }
    ```
*   **Response (Success - 200 OK)**: (Full cart data as in 3.1.1)

#### 3.1.4. Update Item Quantity in User Cart

*   **Endpoint**: `POST /cart/user/update/`
*   **Description**: Updates the quantity of a specific product in the authenticated user's cart.
*   **Authentication Required**: Yes
*   **Request Body**:
    ```json
    {
        "product_id": 101,
        "quantity": 3
    }
    ```
*   **Response (Success - 200 OK)**: (Full cart data as in 3.1.1)

#### 3.1.5. Clear User Cart

*   **Endpoint**: `POST /cart/user/clear/`
*   **Description**: Removes all items from the authenticated user's cart.
*   **Authentication Required**: Yes
*   **Response (Success - 200 OK)**: (Full cart data, likely with an empty `items` array)

### 3.2. Guest Cart Operations (Unauthenticated Users)

*Guest cart operations rely on a `session_key` that the frontend needs to generate and manage for unauthenticated users. This key should be passed in requests.*

#### 3.2.1. Get Guest Cart

*   **Endpoint**: `GET /cart/guest/`
*   **Description**: Retrieves the guest cart associated with a session key.
*   **Authentication Required**: No
*   **Query Parameters**:
    *   `session_key` (required): The unique session key for the guest.
*   **Response (Success - 200 OK)**:
    ```json
    {
        "id": 5, // GuestCart ID
        "session_key": "unique_guest_session_key_abc123",
        "items": [
            {
                "id": 12, // GuestCartItem ID
                "product": { /* Full Product Serializer data */ },
                "product_id": 102,
                "quantity": 1,
                "added_at": "2023-03-01T11:00:00Z"
            }
        ],
        "created_at": "2023-03-01T11:00:00Z",
        "updated_at": "2023-03-01T11:00:00Z"
    }
    ```
*   **Response (Error - 400 Bad Request)**:
    ```json
    {
        "error": "session_key required"
    }
    ```

#### 3.2.2. Add Item to Guest Cart

*   **Endpoint**: `POST /cart/guest/add/`
*   **Description**: Adds a product to the guest cart or updates quantity.
*   **Authentication Required**: No
*   **Request Body**:
    ```json
    {
        "session_key": "unique_guest_session_key_abc123",
        "product_id": 102,
        "quantity": 1 // Optional
    }
    ```
*   **Response (Success - 200 OK)**: (Full guest cart data as in 3.2.1)
*   **Response (Error - 400 Bad Request)**:
    ```json
    {
        "error": "session_key and product_id required"
    }
    ```

#### 3.2.3. Remove Item from Guest Cart

*   **Endpoint**: `POST /cart/guest/remove/`
*   **Description**: Removes a product from the guest cart.
*   **Authentication Required**: No
*   **Request Body**:
    ```json
    {
        "session_key": "unique_guest_session_key_abc123",
        "product_id": 102
    }
    ```
*   **Response (Success - 200 OK)**: (Full guest cart data as in 3.2.1, or empty object if cart becomes empty and is deleted)

#### 3.2.4. Update Item Quantity in Guest Cart

*   **Endpoint**: `POST /cart/guest/update/`
*   **Description**: Updates product quantity in the guest cart.
*   **Authentication Required**: No
*   **Request Body**:
    ```json
    {
        "session_key": "unique_guest_session_key_abc123",
        "product_id": 102,
        "quantity": 2
    }
    ```
*   **Response (Success - 200 OK)**: (Full guest cart data as in 3.2.1)

#### 3.2.5. Clear Guest Cart

*   **Endpoint**: `POST /cart/guest/clear/`
*   **Description**: Removes all items from the guest cart.
*   **Authentication Required**: No
*   **Request Body**:
    ```json
    {
        "session_key": "unique_guest_session_key_abc123"
    }
    ```
*   **Response (Success - 200 OK)**: (Full guest cart data, likely empty `items`)

### 3.3. Merge Guest Cart to User Cart

*   **Endpoint**: `POST /cart/merge/`
*   **Description**: Merges items from a guest cart (identified by `session_key`) into the authenticated user's cart. Typically called after a guest logs in or registers. The guest cart is deleted after successful merge.
*   **Authentication Required**: Yes
*   **Request Body**:
    ```json
    {
        "session_key": "unique_guest_session_key_to_merge"
    }
    ```
*   **Response (Success - 200 OK)**: (The authenticated user's updated cart data, as in 3.1.1)
*   **Response (Error - 400 Bad Request)**:
    ```json
    {
        "error": "session_key required"
    }
    ```
*   **Response (Error - 404 Not Found)**:
    ```json
    {
        "error": "Guest cart not found"
    }
    ```

---

## 4. Orders (`/orders/`)

### 4.1. Create Order (Checkout)

*   **Endpoint**: `POST /checkout/create-order/` (Example path, confirm actual path from main router)
    *   *Note: The current `orders` app structure (`auero_backend_gold/orders/`) does not seem to have a direct "create order from cart" endpoint for users. It has `OrderListView` which is more for listing existing orders. A dedicated checkout endpoint is usually present in a separate `checkout` app or within `orders`.*
    *   *Assuming a standard checkout flow, the request would involve cart items (or a cart ID), shipping address ID, and payment details (though payment is out of scope for this initial spec).*
    *   **This section needs to be defined based on the actual checkout implementation.**
    *   **For now, let's assume an endpoint `POST /orders/orders/` for creating an order, though this is a guess based on `OrderListView` behavior for `GET`.**

    *   **Placeholder Endpoint**: `POST /orders/orders/` (This needs verification and proper definition)
    *   **Description**: Creates a new order from the user's cart items. (This is a simplified representation, actual checkout is more complex)
    *   **Authentication Required**: Yes
    *   **Request Body (Example - Needs Confirmation)**:
        ```json
        {
            // This request body is speculative and needs to align with backend.
            // It likely involves items from the cart, shipping address, etc.
            // For this example, let's assume it takes product_id and quantity similar to order model.
            "product_id": 101, // ID of the product being ordered
            "quantity": 1, // Not in current Order model, implies single item order
            "shipping_address_id": 5, // ID of user's saved address
            "payment_method_id": "stripe_token_or_similar" // If payment was integrated
        }
        ```
        *The current `Order` model seems to represent a single product sale rather than a multi-item cart checkout. The `Order` model has a direct `product` ForeignKey. This implies orders are created per product. The `OrderSerializer` expects `product`, `buyer`, `vendor`, `sale_price`.*

        *If the system is designed for selling individual pre-owned items (consignment model), then creating an "order" might happen when a specific `Product` (which is already approved and has a `selling_price`) is purchased.*

        **Revised interpretation based on `Order` model for a single product purchase:**
    *   **Endpoint**: `POST /orders/orders/` (Assuming this is the creation endpoint)
    *   **Description**: Creates an order for a specific product.
    *   **Authentication Required**: Yes
    *   **Request Body**:
        ```json
        {
            "product_id": 101, // The ID of the Product to purchase
            // sale_price would be derived from the Product's selling_price by the backend
            // buyer would be request.user
            // vendor would be derived from Product.vendor
        }
        ```
    *   **Response (Success - 201 Created)**:
        ```json
        {
            "id": 1, // Order ID
            "product": 101,
            "product_details": { /* Product details as in ProductSerializer */ },
            "buyer": 15, // Buyer User ID
            "buyer_details": { /* UserSerializer data for buyer */ },
            "vendor": 5, // Vendor User ID
            "vendor_details": { /* UserSerializer data for vendor */ },
            "sale_price": "699.99",
            "sale_date": "2023-03-02T12:00:00Z",
            "payout_status": "PENDING",
            "payout": null, // Payout ID, null until processed
            "payout_details": null
        }
        ```

### 4.2. List User Orders

*   **Endpoint**: `GET /orders/orders/`
*   **Description**: Retrieves a list of orders for the authenticated user (as a buyer).
*   **Authentication Required**: Yes
*   **Query Parameters (Optional)**:
    *   `page`, `page_size`: For pagination.
*   **Response (Success - 200 OK)**: (Paginated list of order objects, same structure as 4.1 Response)
    ```json
    [ // Array of order objects if not paginated, or paginated structure
        {
            "id": 1,
            "product": 101,
            "product_details": { /* ... */ },
            "buyer": 15,
            "buyer_details": { /* ... */ },
            "vendor": 5,
            "vendor_details": { /* ... */ },
            "sale_price": "699.99",
            "sale_date": "2023-03-02T12:00:00Z",
            "payout_status": "PENDING",
            "payout": null,
            "payout_details": null
        },
        // ... more orders
    ]
    ```

### 4.3. Get Order Details

*   **Endpoint**: `GET /orders/orders/<int:order_id>/`
*   **Description**: Retrieves details of a specific order placed by the authenticated user.
*   **Authentication Required**: Yes
*   **URL Parameter**: `order_id` - The ID of the order.
*   **Response (Success - 200 OK)**: (Single order object, same structure as 4.1 Response)
*   **Response (Error - 403 Forbidden/404 Not Found)**: If the order does not belong to the user or does not exist.

---

This documentation should provide a good starting point for the mobile app developers. Remember to replace placeholder URLs and confirm any assumptions made about endpoint behavior (especially for order creation). 