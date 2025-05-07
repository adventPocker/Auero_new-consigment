# E-commerce Platform API Documentation

This document provides comprehensive documentation for the backend APIs used by the e-commerce platform for gold and jewelry products.

## Authentication

All protected endpoints require JWT authentication using the Bearer token scheme.

**Header Format:**
```
Authorization: Bearer <your_jwt_token>
```

You can obtain a token using the login endpoint (see Authentication API docs).

---

## Products API

### Categories

#### List All Categories
- **URL**: `/api/products/categories/`
- **Method**: GET
- **Auth Required**: No
- **Response Example**:
```json
[
  {
    "id": 1,
    "name": "Gold Rings",
    "name_ar": "خواتم ذهب",
    "slug": "gold-rings",
    "description": "Gold ring category",
    "description_ar": "فئة خواتم الذهب",
    "banner_image": "http://localhost:8000/media/category_banners/gold-rings.jpg",
    "image": "http://localhost:8000/media/category_images/gold-rings-icon.jpg",
    "parent": null,
    "is_active": true,
    "created_at": "2024-06-01T12:00:00Z",
    "updated_at": "2024-06-01T12:00:00Z"
  }
]
```

#### Create Category
- **URL**: `/api/products/categories/`
- **Method**: POST
- **Auth Required**: Yes (admin)
- **Request Body**:
```json
{
  "name": "Gold Rings",
  "name_ar": "خواتم ذهب",
  "description": "Gold ring category",
  "description_ar": "فئة خواتم الذهب"
}
```
- **Response**: The created category object

#### Get Category Detail
- **URL**: `/api/products/categories/{id}/`
- **Method**: GET
- **Auth Required**: No
- **Response**: Category object

#### Update Category
- **URL**: `/api/products/categories/{id}/`
- **Method**: PUT
- **Auth Required**: Yes (admin)
- **Request Body**:
```json
{
  "name": "Updated Category",
  "name_ar": "فئة محدثة",
  "description": "Updated description",
  "description_ar": "وصف محدث"
}
```
- **Response**: Updated category object

#### Delete Category
- **URL**: `/api/products/categories/{id}/`
- **Method**: DELETE
- **Auth Required**: Yes (admin)
- **Response**: 204 No Content

#### List Products in Category
- **URL**: `/api/products/categories/{id}/products/`
- **Method**: GET
- **Auth Required**: No
- **Response**: List of products in the category

### Products

#### List Products
- **URL**: `/api/products/products/`
- **Method**: GET
- **Auth Required**: Yes
- **Response Example**:
```json
[
  {
    "id": 1,
    "vendor": 5,
    "vendor_name": "John Doe",
    "category": 1,
    "category_name": "Gold Rings",
    "name": "18K Gold Ring",
    "name_ar": "خاتم ذهب 18 قيراط",
    "slug": "18k-gold-ring",
    "description": "A beautiful 18K gold ring.",
    "description_ar": "خاتم جميل من الذهب عيار 18.",
    "vendor_price": "1000.00",
    "selling_price": "1200.00",
    "platform_fee": "120.00",
    "vendor_payout": "1080.00",
    "payout_status": "PENDING",
    "status": "APPROVED",
    "inspection_notes": "",
    "created_at": "2024-06-01T12:00:00Z",
    "updated_at": "2024-06-01T12:00:00Z",
    "images": [
      {
        "id": 1,
        "image": "http://localhost:8000/media/product_images/ring.jpg",
        "is_primary": true,
        "created_at": "2024-06-01T12:00:00Z"
      }
    ],
    "consignment": {
      "id": 1,
      "handover_date": "2024-06-01T12:00:00Z",
      "inspection_date": "2024-06-01T14:00:00Z",
      "physical_status": "INSPECTED",
      "inspector": 1,
      "inspector_name": "Admin User",
      "quality_notes": "Good quality item",
      "authentication_notes": "Authentic gold",
      "created_at": "2024-06-01T12:00:00Z",
      "updated_at": "2024-06-01T14:00:00Z"
    }
  }
]
```

#### Create Product
- **URL**: `/api/products/products/`
- **Method**: POST
- **Auth Required**: Yes (vendor or admin)
- **Request Body**:
```json
{
  "category": 1,
  "name": "18K Gold Ring",
  "name_ar": "خاتم ذهب 18 قيراط",
  "description": "A beautiful 18K gold ring.",
  "description_ar": "خاتم جميل من الذهب عيار 18.",
  "vendor_price": "1000.00"
}
```
- **Response**: Created product object

#### Get Product Detail
- **URL**: `/api/products/products/{id}/`
- **Method**: GET
- **Auth Required**: Yes
- **Response**: Product object

#### Update Product
- **URL**: `/api/products/products/{id}/`
- **Method**: PUT
- **Auth Required**: Yes (owner vendor or admin)
- **Request Body**:
```json
{
  "category": 1,
  "name": "Updated Product",
  "name_ar": "منتج محدث",
  "description": "Updated description",
  "description_ar": "وصف محدث",
  "vendor_price": "1200.00",
  "selling_price": "1500.00",
  "status": "APPROVED"
}
```
- **Response**: Updated product object

#### Mark Product as Sold
- **URL**: `/api/products/products/{id}/`
- **Method**: PUT
- **Auth Required**: Yes (admin)
- **Request Body**:
```json
{
  "status": "SOLD"
}
```
- **Response**: Updated product object with calculated platform_fee and vendor_payout

#### Delete Product
- **URL**: `/api/products/products/{id}/`
- **Method**: DELETE
- **Auth Required**: Yes (owner vendor or admin)
- **Response**: 204 No Content

#### Upload Product Images
- **URL**: `/api/products/products/{id}/images/`
- **Method**: POST
- **Auth Required**: Yes (owner vendor or admin)
- **Request Body**: FormData with:
  - `images`: File(s)
  - `is_primary`: Boolean (optional)
- **Response**: List of uploaded image objects

### Consignments

#### List Consignments
- **URL**: `/api/products/consignments/`
- **Method**: GET
- **Auth Required**: Yes
- **Response**: List of consignments (filtered by user role)

#### Create Consignment
- **URL**: `/api/products/consignments/`
- **Method**: POST
- **Auth Required**: Yes (vendor or admin)
- **Request Body**:
```json
{
  "product": 1,
  "handover_date": "2024-06-01T13:00:00Z",
  "physical_status": "DELIVERED",
  "quality_notes": "Excellent condition.",
  "authentication_notes": "Genuine gold."
}
```
- **Response**: Created consignment object

#### Get Consignment Detail
- **URL**: `/api/products/consignments/{id}/`
- **Method**: GET
- **Auth Required**: Yes (owner vendor or admin)
- **Response**: Consignment object

#### Update Consignment
- **URL**: `/api/products/consignments/{id}/`
- **Method**: PUT
- **Auth Required**: Yes (owner vendor or admin)
- **Request Body**:
```json
{
  "handover_date": "2024-06-01T13:00:00Z",
  "inspection_date": "2024-06-01T14:00:00Z",
  "physical_status": "INSPECTED",
  "quality_notes": "Checked and approved.",
  "authentication_notes": "Verified."
}
```
- **Response**: Updated consignment object

#### Update Consignment Status
- **URL**: `/api/products/consignments/{id}/status/`
- **Method**: POST
- **Auth Required**: Yes (admin)
- **Request Body**:
```json
{
  "physical_status": "SOLD"
}
```
- **Response**: Updated consignment object

### Product Search

#### Search Products
- **URL**: `/api/products/search/`
- **Method**: GET
- **Auth Required**: No
- **Query Parameters**:
  - `q`: Text search query (name, description, category)
  - `category`: Category ID filter
  - `min_price`: Minimum price
  - `max_price`: Maximum price
  - `status`: Product status
  - `ordering`: Field to order by (e.g., `-selling_price`, `created_at`)
  - `page`: Page number
  - `page_size`: Items per page
- **Example Request**:
```
/api/products/search/?q=gold&category=1&min_price=1000&max_price=5000&status=APPROVED&ordering=-selling_price&page=1&page_size=10
```
- **Response Example**:
```json
{
  "count": 5,
  "next": "http://localhost:8000/api/products/search/?page=2&page_size=10",
  "previous": null,
  "results": [
    {
      "id": 1,
      "name": "18K Gold Ring",
      "selling_price": "1200.00",
      "status": "APPROVED",
      "images": [{ "image": "http://localhost:8000/media/product_images/ring.jpg" }]
    }
  ]
}
```

---

## Orders API

### Orders

#### List Orders
- **URL**: `/api/orders/orders/`
- **Method**: GET
- **Auth Required**: Yes
- **Notes**: Admin sees all orders, vendors see their sales, regular users see their purchases
- **Response Example**:
```json
[
  {
    "id": 1,
    "product": 5,
    "product_details": {
      "id": 5,
      "name": "18K Gold Ring",
      "vendor_price": "1000.00",
      "selling_price": "1200.00",
      "platform_fee": "120.00",
      "vendor_payout": "1080.00"
    },
    "buyer": 7,
    "buyer_details": {
      "id": 7,
      "username": "customer1",
      "email": "customer1@example.com",
      "full_name": "John Customer"
    },
    "vendor": 5,
    "vendor_details": {
      "id": 5,
      "username": "vendor1",
      "email": "vendor1@example.com",
      "full_name": "Jane Vendor"
    },
    "sale_price": "1200.00",
    "sale_date": "2024-06-15T12:00:00Z",
    "payout_status": "PENDING",
    "payout": null,
    "payout_details": null
  }
]
```

#### Get Order Detail
- **URL**: `/api/orders/orders/{id}/`
- **Method**: GET
- **Auth Required**: Yes (admin, buyer, or vendor)
- **Response**: Order object with details

### Payouts

#### List Payouts
- **URL**: `/api/orders/payouts/`
- **Method**: GET
- **Auth Required**: Yes
- **Notes**: Admin sees all payouts, vendors see only their payouts
- **Response Example**:
```json
[
  {
    "id": 1,
    "product": 5,
    "product_name": "18K Gold Ring",
    "vendor": 5,
    "vendor_name": "Jane Vendor",
    "amount": "1080.00",
    "date": "2024-06-16T14:30:00Z",
    "method": "Bank Transfer",
    "notes": "Paid via bank transfer on June 16, 2024"
  }
]
```

#### Get Payout Detail
- **URL**: `/api/orders/payouts/{id}/`
- **Method**: GET
- **Auth Required**: Yes (admin or recipient vendor)
- **Response**: Payout object with details

#### Mark Payout as Paid
- **URL**: `/api/orders/orders/{id}/mark-paid/`
- **Method**: POST
- **Auth Required**: Yes (admin only)
- **Request Body**:
```json
{
  "method": "Bank Transfer",
  "notes": "Paid via bank transfer on June 15, 2024"
}
```
- **Response**: Updated order object with payout details

## Response Status Codes

- `200 OK`: Request succeeded
- `201 Created`: Resource created successfully
- `204 No Content`: Resource deleted successfully
- `400 Bad Request`: Invalid request data
- `401 Unauthorized`: Authentication failed
- `403 Forbidden`: Authentication succeeded but user lacks permission
- `404 Not Found`: Resource not found
- `500 Internal Server Error`: Unexpected server error 