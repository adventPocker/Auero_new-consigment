# Products API Documentation

## Authentication
All endpoints require authentication using JWT token. Include the token in the Authorization header:
```
Authorization: Bearer <your_token>
```

## Categories

### List Categories
- **URL**: `/api/categories/`
- **Method**: GET
- **Auth Required**: Yes
- **Permissions**: Authenticated users
- **Response**: List of all categories
```json
[
  {
    "id": 1,
    "name": "string",
    "name_ar": "string",
    "slug": "string",
    "description": "string",
    "description_ar": "string",
    "banner_image": "url",
    "image": "url",
    "parent": null,
    "is_active": true,
    "created_at": "datetime",
    "updated_at": "datetime"
  }
]
```

### Create Category
- **URL**: `/api/categories/`
- **Method**: POST
- **Auth Required**: Yes
- **Permissions**: Admin users only
- **Request Body**:
```json
{
  "name": "string",
  "name_ar": "string",
  "description": "string",
  "description_ar": "string",
  "banner_image": "file",
  "image": "file",
  "is_active": true
}
```

### Get Category Detail
- **URL**: `/api/categories/{id}/`
- **Method**: GET
- **Auth Required**: Yes
- **Permissions**: Authenticated users
- **Response**: Single category details

### Update Category
- **URL**: `/api/categories/{id}/`
- **Method**: PUT
- **Auth Required**: Yes
- **Permissions**: Admin users only
- **Request Body**: Same as Create Category

### Delete Category
- **URL**: `/api/categories/{id}/`
- **Method**: DELETE
- **Auth Required**: Yes
- **Permissions**: Admin users only

### List Category Products
- **URL**: `/api/categories/{id}/products/`
- **Method**: GET
- **Auth Required**: Yes
- **Permissions**: Authenticated users
- **Response**: List of products in the category

## Products

### List Products
- **URL**: `/api/products/`
- **Method**: GET
- **Auth Required**: Yes
- **Permissions**: 
  - Admin users: See all products
  - Vendors: See only their products
- **Response**: List of products
```json
[
  {
    "id": 1,
    "vendor": 1,
    "vendor_name": "string",
    "category": 1,
    "category_name": "string",
    "name": "string",
    "name_ar": "string",
    "slug": "string",
    "description": "string",
    "description_ar": "string",
    "vendor_price": "decimal",
    "selling_price": "decimal",
    "status": "string",
    "inspection_notes": "string",
    "created_at": "datetime",
    "updated_at": "datetime",
    "images": [],
    "consignment": null
  }
]
```

### Create Product
- **URL**: `/api/products/`
- **Method**: POST
- **Auth Required**: Yes
- **Permissions**: Authenticated users
- **Request Body**:
```json
{
  "category": 1,
  "name": "string",
  "name_ar": "string",
  "description": "string",
  "description_ar": "string",
  "vendor_price": "decimal"
}
```

### Get Product Detail
- **URL**: `/api/products/{id}/`
- **Method**: GET
- **Auth Required**: Yes
- **Permissions**: 
  - Admin users: Access any product
  - Vendors: Access only their products

### Update Product
- **URL**: `/api/products/{id}/`
- **Method**: PUT
- **Auth Required**: Yes
- **Permissions**: 
  - Admin users: Update any product
  - Vendors: Update only their products

### Delete Product
- **URL**: `/api/products/{id}/`
- **Method**: DELETE
- **Auth Required**: Yes
- **Permissions**: 
  - Admin users: Delete any product
  - Vendors: Delete only their products

### Upload Product Images
- **URL**: `/api/products/{id}/images/`
- **Method**: POST
- **Auth Required**: Yes
- **Permissions**: 
  - Admin users: Upload for any product
  - Vendors: Upload only for their products
- **Request Body**: Form data with:
  - `images`: List of image files
  - `is_primary`: Boolean (optional)

## Consignments

### List Consignments
- **URL**: `/api/consignments/`
- **Method**: GET
- **Auth Required**: Yes
- **Permissions**: 
  - Admin users: See all consignments
  - Vendors: See only their consignments
- **Response**: List of consignments
```json
[
  {
    "id": 1,
    "handover_date": "datetime",
    "inspection_date": "datetime",
    "physical_status": "string",
    "inspector": 1,
    "inspector_name": "string",
    "quality_notes": "string",
    "authentication_notes": "string",
    "created_at": "datetime",
    "updated_at": "datetime"
  }
]
```

### Create Consignment
- **URL**: `/api/consignments/`
- **Method**: POST
- **Auth Required**: Yes
- **Permissions**: Authenticated users
- **Request Body**:
```json
{
  "handover_date": "datetime",
  "physical_status": "string",
  "quality_notes": "string",
  "authentication_notes": "string"
}
```

### Get Consignment Detail
- **URL**: `/api/consignments/{id}/`
- **Method**: GET
- **Auth Required**: Yes
- **Permissions**: 
  - Admin users: Access any consignment
  - Vendors: Access only their consignments

### Update Consignment
- **URL**: `/api/consignments/{id}/`
- **Method**: PUT
- **Auth Required**: Yes
- **Permissions**: 
  - Admin users: Update any consignment
  - Vendors: Update only their consignments

### Delete Consignment
- **URL**: `/api/consignments/{id}/`
- **Method**: DELETE
- **Auth Required**: Yes
- **Permissions**: 
  - Admin users: Delete any consignment
  - Vendors: Delete only their consignments

### Update Consignment Status
- **URL**: `/api/consignments/{id}/status/`
- **Method**: PUT
- **Auth Required**: Yes
- **Permissions**: 
  - Admin users: Update any consignment status
  - Vendors: View only

## Status Enums

### Product Submission Status
- `DRAFT`: Initial state
- `SUBMITTED`: Submitted for review
- `INSPECTION`: Under inspection
- `APPROVED`: Approved for sale
- `REJECTED`: Rejected
- `SOLD`: Product has been sold

### Consignment Physical Status
- `PENDING`: Pending delivery
- `DELIVERED`: Delivered to admin
- `INSPECTED`: Inspection complete
- `RETURNED`: Returned to vendor
- `SOLD`: Sold to customer
