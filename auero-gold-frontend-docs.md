# Auero Gold Frontend Development Documentation

## Project Overview

Auero Gold is a specialized e-commerce platform for gold and jewelry products that connects vendors with customers. The platform allows vendors to list their products, and customers can browse, search, and purchase them.

## Technical Stack

- **Frontend**: Next.js (latest version)
- **API Communication**: RESTful API
- **Authentication**: JWT (JSON Web Tokens)
- **State Management**: Recommended to use React Context API or Redux Toolkit
- **Styling**: Your choice of Tailwind CSS, MUI, or any other modern UI framework

## Getting Started

1. Create a new Next.js application:
   ```bash
   npx create-next-app@latest auero-gold-frontend
   ```

2. Configure environment variables in `.env.local`:
   ```
   NEXT_PUBLIC_API_BASE_URL=http://localhost:8000
   ```

3. Set up folders structure:
   ```
   src/
   ├── components/        # Reusable UI components
   ├── contexts/          # React Context providers
   ├── hooks/             # Custom React hooks
   ├── layouts/           # Page layouts
   ├── pages/             # Next.js pages
   ├── services/          # API service functions
   ├── styles/            # Global styles
   └── utils/             # Utility functions
   ```

## Authentication Flow

The application uses JWT authentication with access and refresh tokens:

1. **Access Token**: Short-lived token (typically expires in 15-30 minutes)
2. **Refresh Token**: Long-lived token used to get new access tokens when they expire

### Implementation Guidelines:

1. Create an authentication context to manage auth state globally
2. Implement token storage in localStorage or cookies
3. Create axios interceptors to:
   - Add Authorization headers to requests
   - Handle 401 errors by attempting token refresh
   - Redirect to login page if refresh fails

## API Module Documentation

### 1. Authentication API

Base URL: `/api/auth`

#### Endpoints:

| Endpoint | Method | Description | Request Body | Response |
|----------|--------|-------------|--------------|----------|
| `/signup/customer/` | POST | Register a new customer | `{ username, email, password, user_type }` | `{ status, message, user, tokens }` |
| `/signup/vendor/` | POST | Register a new vendor | Form data with user details and vendor profile | `{ status, message, user, tokens }` |
| `/login/` | POST | Login a user | `{ email, password }` | `{ user, tokens }` |
| `/refresh-token/` | POST | Get a new access token | `{ refresh }` | `{ access }` |
| `/logout/` | POST | Logout and invalidate tokens | `{ refresh_token }` | `{ status, message }` |
| `/me/` | GET | Get current user info | - | `{ status, user }` |
| `/addresses/` | GET | List user addresses | - | Array of addresses |
| `/addresses/` | POST | Create a new address | Address details | Created address |
| `/addresses/:id/` | GET | Get address details | - | Address object |
| `/addresses/:id/` | PUT | Update address | Address details | Updated address |
| `/addresses/:id/` | DELETE | Delete address | - | - |

### 2. Products API

Base URL: `/api/products`

#### Endpoints:

| Endpoint | Method | Description | Auth Required | Response |
|----------|--------|-------------|---------------|----------|
| `/categories/` | GET | List all categories | No | Array of categories |
| `/categories/` | POST | Create a category | Yes (Admin) | Created category |
| `/categories/:id/` | GET | Get category details | No | Category object |
| `/categories/:id/` | PUT | Update a category | Yes (Admin) | Updated category |
| `/categories/:id/` | DELETE | Delete a category | Yes (Admin) | - |
| `/categories/:id/products/` | GET | List products in category | No | Array of products |
| `/products/` | GET | List all products | Yes | Array of products |
| `/products/` | POST | Create a product | Yes (Vendor) | Created product |
| `/products/:id/` | GET | Get product details | Yes | Product object |
| `/products/:id/` | PUT | Update a product | Yes (Owner) | Updated product |
| `/products/:id/` | DELETE | Delete a product | Yes (Owner) | - |
| `/products/:id/images/` | POST | Upload product images | Yes (Owner) | Upload response |
| `/consignments/` | GET | List consignments | Yes | Array of consignments |
| `/consignments/` | POST | Create a consignment | Yes | Created consignment |
| `/consignments/:id/` | GET | Get consignment details | Yes | Consignment object |
| `/consignments/:id/` | PUT | Update a consignment | Yes | Updated consignment |
| `/consignments/:id/` | DELETE | Delete a consignment | Yes | - |
| `/consignments/:id/status/` | POST | Update consignment status | Yes | Updated status |
| `/search/` | GET | Search products | No | Search results |

### 3. Cart API

Base URL: `/api/cart`

#### Endpoints:

| Endpoint | Method | Description | Auth Required | Response |
|----------|--------|-------------|---------------|----------|
| `/user/` | GET | Get user cart | Yes | Cart with items |
| `/user/add/` | POST | Add to user cart | Yes | `{ product_id, quantity }` |
| `/user/remove/` | POST | Remove from user cart | Yes | `{ product_id }` |
| `/user/update/` | POST | Update item quantity | Yes | `{ product_id, quantity }` |
| `/user/clear/` | POST | Clear user cart | Yes | - |
| `/guest/` | GET | Get guest cart | No | Query param: `session_key` |
| `/guest/add/` | POST | Add to guest cart | No | `{ session_key, product_id, quantity }` |
| `/guest/remove/` | POST | Remove from guest cart | No | `{ session_key, product_id }` |
| `/guest/update/` | POST | Update guest cart item | No | `{ session_key, product_id, quantity }` |
| `/guest/clear/` | POST | Clear guest cart | No | `{ session_key }` |
| `/merge/` | POST | Merge guest cart into user | Yes | `{ session_key }` |

### 4. Orders API

Base URL: `/api/orders`

#### Endpoints:

| Endpoint | Method | Description | Auth Required | Response |
|----------|--------|-------------|---------------|----------|
| `/orders/` | GET | List user orders | Yes | Array of orders |
| `/orders/:id/` | GET | Get order details | Yes | Order object |
| `/payouts/` | GET | List payouts | Yes (Vendor) | Array of payouts |
| `/payouts/:id/` | GET | Get payout details | Yes (Vendor) | Payout object |
| `/orders/:id/mark-paid/` | POST | Mark order as paid | Yes (Admin) | `{ method, notes }` |

## Implementation Guidelines

### 1. Authentication & User Management

1. Create login, registration, and profile pages
2. Implement protected routes for authenticated users
3. Create a global auth context with:
   - Current user state
   - Login/logout functions
   - Token refresh mechanism

### 2. Product Browsing

1. Create category browsing with filtering
2. Implement product search with filters:
   - Price range
   - Category
   - Status
3. Create product detail pages with images and details

### 3. Cart Management

1. Implement persistent cart:
   - For guests: Use local storage with session key
   - For users: Use server-side cart
2. Create add/remove/update functionality
3. Implement cart merging when guest logs in

### 4. Vendor Dashboard

1. Create product management interface:
   - List products
   - Add/edit products
   - Upload images
2. Implement consignment tracking
3. Create order and payout views

### 5. Customer Flow

1. Create shopping cart and checkout process
2. Implement address management
3. Create order history and tracking pages

## API Error Handling

- All API responses include a status code and message
- Handle common errors:
  - 400: Bad Request (validation error)
  - 401: Unauthorized (not logged in)
  - 403: Forbidden (insufficient permissions)
  - 404: Not Found
  - 500: Server Error

Implement a global error handler that:
1. Shows appropriate error messages to users
2. Logs errors for debugging
3. Redirects to login on authentication failures

## Multilingual Support

The API supports both English and Arabic content:
- Products have `name`/`name_ar` and `description`/`description_ar` fields
- Categories have similar dual language fields
- Implement language toggle in UI and display appropriate fields

## API Request Examples

### Login Request

```javascript
const login = async (email, password) => {
  try {
    const response = await axios.post('/api/auth/login/', { email, password });
    // Store tokens
    localStorage.setItem('accessToken', response.data.tokens.access);
    localStorage.setItem('refreshToken', response.data.tokens.refresh);
    // Store user data
    return response.data.user;
  } catch (error) {
    // Handle login errors
    throw error;
  }
};
```

### Product Search Request

```javascript
const searchProducts = async (params) => {
  try {
    const response = await axios.get('/api/products/search/', { params });
    return response.data;
  } catch (error) {
    // Handle search errors
    throw error;
  }
};

// Example usage
searchProducts({
  q: 'gold',
  category: 1,
  min_price: 1000,
  max_price: 5000,
  status: 'APPROVED',
  ordering: '-selling_price',
  page: 1,
  page_size: 10
});
```

### Adding to Cart

```javascript
// For authenticated users
const addToUserCart = async (productId, quantity) => {
  try {
    const response = await axios.post('/api/cart/user/add/', {
      product_id: productId,
      quantity: quantity
    });
    return response.data;
  } catch (error) {
    // Handle errors
    throw error;
  }
};

// For guest users
const addToGuestCart = async (sessionKey, productId, quantity) => {
  try {
    const response = await axios.post('/api/cart/guest/add/', {
      session_key: sessionKey,
      product_id: productId,
      quantity: quantity
    });
    return response.data;
  } catch (error) {
    // Handle errors
    throw error;
  }
};
```

## Best Practices

1. **Use TypeScript** for better type safety and developer experience
2. **Implement proper loading states** for all API calls
3. **Create reusable components** for common UI elements
4. **Setup proper API service layer** to separate API logic from components
5. **Use React Query or SWR** for data fetching, caching, and state management
6. **Implement proper form validation** using libraries like Formik or React Hook Form
7. **Set up proper SEO** with Next.js metadata API
8. **Create responsive designs** that work well on mobile and desktop
9. **Implement proper error boundary components** to catch and handle JS errors
10. **Create a consistent design system** with reusable styles and components

## Testing Guidelines

1. Set up Jest and React Testing Library
2. Write unit tests for key components
3. Implement integration tests for important user flows
4. Create mock services for API endpoints

## Deployment Considerations

1. Configure CI/CD pipeline
2. Set up environment variables for different environments
3. Implement proper build and deployment scripts
4. Consider using Next.js API routes for BFF (Backend for Frontend) patterns

## Security Best Practices

1. Never store sensitive information in localStorage
2. Implement proper CSRF protection
3. Sanitize user inputs
4. Use HTTPS for all API calls
5. Properly handle JWT tokens and implement secure refresh mechanisms 