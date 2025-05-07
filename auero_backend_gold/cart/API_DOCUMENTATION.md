# Auero Cart API Documentation

## Base URL

```
http://localhost:8000/api/cart/
```

---

## Authentication

- **User Cart Endpoints:** Require JWT Bearer token in the `Authorization` header.
- **Guest Cart Endpoints:** No authentication required, but a `session_key` is mandatory.

---

## Endpoints Overview

| Endpoint                  | Method | Auth Required | Description                                 |
|---------------------------|--------|---------------|---------------------------------------------|
| user/                     | GET    | Yes           | Get current user's cart                     |
| user/add/                 | POST   | Yes           | Add item to user cart                       |
| user/remove/              | POST   | Yes           | Remove item from user cart                  |
| user/update/              | POST   | Yes           | Update item quantity in user cart           |
| user/clear/               | POST   | Yes           | Clear all items from user cart              |
| guest/                    | GET    | No            | Get guest cart by session key               |
| guest/add/                | POST   | No            | Add item to guest cart                      |
| guest/remove/             | POST   | No            | Remove item from guest cart                 |
| guest/update/             | POST   | No            | Update item quantity in guest cart          |
| guest/clear/              | POST   | No            | Clear all items from guest cart             |
| merge/                    | POST   | Yes           | Merge guest cart into user cart             |

---

## 1. User Cart Endpoints

### 1.1 Get User Cart

**GET** `/user/`

- **Headers:**  
  `Authorization: Bearer <access_token>`

**Response Example:**
```json
{
  "id": 1,
  "user": 2,
  "items": [
    {
      "id": 10,
      "product": {
        "id": 5,
        "name": "Product Name"
        // ...other product fields
      },
      "quantity": 2,
      "added_at": "2024-06-01T12:34:56Z"
    }
  ],
  "created_at": "2024-06-01T12:00:00Z",
  "updated_at": "2024-06-01T12:34:56Z"
}
```

---

### 1.2 Add Item to User Cart

**POST** `/user/add/`

- **Headers:**  
  `Authorization: Bearer <access_token>`  
  `Content-Type: application/json`

- **Body:**
```json
{
  "product_id": 5,
  "quantity": 2
}
```

**Response:** Returns the updated cart (see above).

---

### 1.3 Remove Item from User Cart

**POST** `/user/remove/`

- **Headers:**  
  `Authorization: Bearer <access_token>`  
  `Content-Type: application/json`

- **Body:**
```json
{
  "product_id": 5
}
```

**Response:** Returns the updated cart.

---

### 1.4 Update Item Quantity in User Cart

**POST** `/user/update/`

- **Headers:**  
  `Authorization: Bearer <access_token>`  
  `Content-Type: application/json`

- **Body:**
```json
{
  "product_id": 5,
  "quantity": 3
}
```

**Response:** Returns the updated cart.

---

### 1.5 Clear User Cart

**POST** `/user/clear/`

- **Headers:**  
  `Authorization: Bearer <access_token>`

**Response:** Returns the now-empty cart.

---

## 2. Guest Cart Endpoints

### 2.1 Get Guest Cart

**GET** `/guest/?session_key=abc123`

- **Query Params:**  
  `session_key` (required)

**Response Example:**
```json
{
  "id": 2,
  "session_key": "abc123",
  "items": [
    {
      "id": 11,
      "product": {
        "id": 5,
        "name": "Product Name"
        // ...other product fields
      },
      "quantity": 2,
      "added_at": "2024-06-01T12:34:56Z"
    }
  ],
  "created_at": "2024-06-01T12:00:00Z",
  "updated_at": "2024-06-01T12:34:56Z"
}
```

---

### 2.2 Add Item to Guest Cart

**POST** `/guest/add/`

- **Headers:**  
  `Content-Type: application/json`

- **Body:**
```json
{
  "session_key": "abc123",
  "product_id": 5,
  "quantity": 2
}
```

**Response:** Returns the updated guest cart.

---

### 2.3 Remove Item from Guest Cart

**POST** `/guest/remove/`

- **Headers:**  
  `Content-Type: application/json`

- **Body:**
```json
{
  "session_key": "abc123",
  "product_id": 5
}
```

**Response:** Returns the updated guest cart.

---

### 2.4 Update Item Quantity in Guest Cart

**POST** `/guest/update/`

- **Headers:**  
  `Content-Type: application/json`

- **Body:**
```json
{
  "session_key": "abc123",
  "product_id": 5,
  "quantity": 3
}
```

**Response:** Returns the updated guest cart.

---

### 2.5 Clear Guest Cart

**POST** `/guest/clear/`

- **Headers:**  
  `Content-Type: application/json`

- **Body:**
```json
{
  "session_key": "abc123"
}
```

**Response:** Returns the now-empty guest cart.

---

## 3. Merge Guest Cart into User Cart

**POST** `/merge/`

- **Headers:**  
  `Authorization: Bearer <access_token>`  
  `Content-Type: application/json`

- **Body:**
```json
{
  "session_key": "abc123"
}
```

**Response:** Returns the updated user cart with guest cart items merged in.

---

## Error Responses

- Missing required fields (e.g., `session_key`, `product_id`) will return:
```json
{
  "error": "session_key and product_id required"
}
```
- If a guest cart is not found:
```json
{
  "error": "Guest cart not found"
}
```
- HTTP status codes:  
  - `400` for bad requests  
  - `404` for not found  
  - `401` for unauthorized (user endpoints)

---

## Notes for Frontend Developers

- **session_key**: For guests, generate and persist a unique session key (e.g., in localStorage or cookies).
- **Authorization**: For user endpoints, always include the JWT token.
- **Cart Structure**: Both user and guest carts return a similar structure, making it easy to reuse UI components.
- **Merging Carts**: After login, call `/merge/` to combine guest and user carts, then clear the guest cart on the frontend.
- **Product Details**: The `product` field in cart items contains the full product object (as per your `ProductSerializer`).

---

## Example Workflow

1. **Guest adds items:**  
   - Use `/guest/add/` with a session key.
2. **User logs in:**  
   - Call `/merge/` with the session key to transfer guest cart items to the user cart.
3. **User continues shopping:**  
   - Use `/user/add/`, `/user/update/`, etc., with the JWT token.

---

If you need more details on the product object or authentication, let me know! 