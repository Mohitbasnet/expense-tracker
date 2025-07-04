# Django Expense Tracker API Documentation

## Base URL
```
http://127.0.0.1:8000
```

## Authentication
All protected endpoints require JWT authentication. Include the access token in the Authorization header:
```
Authorization: Bearer <access_token>
```

---

## Authentication Endpoints

### 1. User Registration
**POST** `/api/auth/register/`

Register a new user account.

**Request Body:**
```json
{
  "username": "johndoe",
  "email": "john@example.com",
  "first_name": "John",
  "last_name": "Doe",
  "password": "securepass123",
  "password_confirm": "securepass123"
}
```

**Response (201 Created):**
```json
{
  "message": "User created successfully",
  "user": {
    "id": 1,
    "username": "johndoe",
    "email": "john@example.com",
    "first_name": "John",
    "last_name": "Doe"
  },
  "tokens": {
    "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc...",
    "access": "eyJ0eXAiOiJKV1QiLCJhbGc..."
  }
}
```

**Validation Errors (400 Bad Request):**
```json
{
  "email": ["User with this email already exists"],
  "non_field_errors": ["Passwords don't match"]
}
```

---

### 2. User Login
**POST** `/api/auth/login/`

Authenticate user and receive JWT tokens.

**Request Body:**
```json
{
  "username": "johndoe",
  "password": "securepass123"
}
```

**Response (200 OK):**
```json
{
  "message": "Login successful",
  "user": {
    "id": 1,
    "username": "johndoe",
    "email": "john@example.com",
    "first_name": "John",
    "last_name": "Doe"
  },
  "tokens": {
    "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc...",
    "access": "eyJ0eXAiOiJKV1QiLCJhbGc..."
  }
}
```

**Authentication Errors (400 Bad Request):**
```json
{
  "non_field_errors": ["Invalid credentials"]
}
```

---

### 3. Token Refresh
**POST** `/api/auth/refresh/`

Refresh JWT access token using refresh token.

**Request Body:**
```json
{
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

**Response (200 OK):**
```json
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

---

## Expense/Income Endpoints

### 1. List Expenses/Income
**GET** `/api/expenses/`

Retrieve paginated list of user's expense/income records.

**Headers:**
```
Authorization: Bearer <access_token>
```

**Query Parameters:**
- `page` (optional): Page number for pagination

**Response (200 OK):**
```json
{
  "count": 25,
  "next": "http://127.0.0.1:8000/api/expenses/?page=2",
  "previous": null,
  "results": [
    {
      "id": 1,
      "title": "Grocery Shopping",
      "amount": "100.00",
      "transaction_type": "debit",
      "total": "110.00",
      "created_at": "2025-01-01T10:00:00Z"
    },
    {
      "id": 2,
      "title": "Salary",
      "amount": "3000.00",
      "transaction_type": "credit",
      "total": "3150.00",
      "created_at": "2025-01-01T09:00:00Z"
    }
  ]
}
```

---

### 2. Create Expense/Income
**POST** `/api/expenses/`

Create a new expense or income record.

**Headers:**
```
Authorization: Bearer <access_token>
Content-Type: application/json
```

**Request Body:**
```json
{
  "title": "Grocery Shopping",
  "description": "Weekly groceries from supermarket",
  "amount": "100.00",
  "transaction_type": "debit",
  "tax": "10.00",
  "tax_type": "flat"
}
```

**Field Descriptions:**
- `title` (required): Transaction title (max 200 chars)
- `description` (optional): Detailed description
- `amount` (required): Transaction amount (decimal)
- `transaction_type` (required): "credit" or "debit"
- `tax` (optional): Tax amount (default: 0)
- `tax_type` (optional): "flat" or "percentage" (default: "flat")

**Response (201 Created):**
```json
{
  "id": 1,
  "title": "Grocery Shopping",
  "description": "Weekly groceries from supermarket",
  "amount": "100.00",
  "transaction_type": "debit",
  "tax": "10.00",
  "tax_type": "flat",
  "total": "110.00",
  "created_at": "2025-01-01T10:00:00Z",
  "updated_at": "2025-01-01T10:00:00Z"
}
```

**Validation Errors (400 Bad Request):**
```json
{
  "title": ["This field is required."],
  "amount": ["This field is required."],
  "transaction_type": ["\"invalid\" is not a valid choice."]
}
```

---

### 3. Retrieve Specific Expense/Income
**GET** `/api/expenses/{id}/`

Retrieve details of a specific expense/income record.

**Headers:**
```
Authorization: Bearer <access_token>
```

**Response (200 OK):**
```json
{
  "id": 1,
  "title": "Grocery Shopping",
  "description": "Weekly groceries from supermarket",
  "amount": "100.00",
  "transaction_type": "debit",
  "tax": "10.00",
  "tax_type": "flat",
  "total": "110.00",
  "created_at": "2025-01-01T10:00:00Z",
  "updated_at": "2025-01-01T10:00:00Z"
}
```

**Not Found (404 Not Found):**
```json
{
  "detail": "Not found."
}
```

---

### 4. Update Expense/Income
**PUT** `/api/expenses/{id}/`

Update an existing expense/income record (full update).

**Headers:**
```
Authorization: Bearer <access_token>
Content-Type: application/json
```

**Request Body:**
```json
{
  "title": "Updated Grocery Shopping",
  "description": "Monthly groceries from supermarket",
  "amount": "150.00",
  "transaction_type": "debit",
  "tax": "5.00",
  "tax_type": "percentage"
}
```

**Response (200 OK):**
```json
{
  "id": 1,
  "title": "Updated Grocery Shopping",
  "description": "Monthly groceries from supermarket",
  "amount": "150.00",
  "transaction_type": "debit",
  "tax": "5.00",
  "tax_type": "percentage",
  "total": "157.50",
  "created_at": "2025-01-01T10:00:00Z",
  "updated_at": "2025-01-01T11:00:00Z"
}
```

---

### 5. Partial Update Expense/Income
**PATCH** `/api/expenses/{id}/`

Partially update an existing expense/income record.

**Headers:**
```
Authorization: Bearer <access_token>
Content-Type: application/json
```

**Request Body:**
```json
{
  "title": "Updated Title Only"
}
```

**Response (200 OK):**
```json
{
  "id": 1,
  "title": "Updated Title Only",
  "description": "Weekly groceries from supermarket",
  "amount": "100.00",
  "transaction_type": "debit",
  "tax": "10.00",
  "tax_type": "flat",
  "total": "110.00",
  "created_at": "2025-01-01T10:00:00Z",
  "updated_at": "2025-01-01T11:30:00Z"
}
```

---

### 6. Delete Expense/Income
**DELETE** `/api/expenses/{id}/`

Delete an expense/income record.

**Headers:**
```
Authorization: Bearer <access_token>
```

**Response (204 No Content):**
```
(No response body)
```

---

## Tax Calculation Examples

### Flat Tax
```json
{
  "amount": "100.00",
  "tax": "10.00",
  "tax_type": "flat"
}
```
**Calculation:** Total = 100.00 + 10.00 = **110.00**

### Percentage Tax
```json
{
  "amount": "100.00",
  "tax": "10.00",
  "tax_type": "percentage"
}
```
**Calculation:** Total = 100.00 + (100.00 × 10 ÷ 100) = 100.00 + 10.00 = **110.00**

### Zero Tax
```json
{
  "amount": "100.00",
  "tax": "0.00",
  "tax_type": "flat"
}
```
**Calculation:** Total = 100.00 + 0.00 = **100.00**

---

## Error Responses

### Authentication Required (401 Unauthorized)
```json
{
  "detail": "Authentication credentials were not provided."
}
```

### Permission Denied (403 Forbidden)
```json
{
  "detail": "You do not have permission to perform this action."
}
```

### Not Found (404 Not Found)
```json
{
  "detail": "Not found."
}
```

### Validation Error (400 Bad Request)
```json
{
  "field_name": ["Error message for this field"],
  "non_field_errors": ["General validation error"]
}
```

---

## User Permissions

### Regular Users
- Can only view, create, update, and delete their own expense/income records
- Cannot access other users' data
- Automatically filtered in list views

### Superusers
- Can access all users' expense/income records
- Can perform all CRUD operations on any record
- See all records in list views

---

## Pagination

List endpoints return paginated results with the following structure:

```json
{
  "count": 25,                    // Total number of records
  "next": "http://...?page=2",    // URL for next page (null if last page)
  "previous": null,               // URL for previous page (null if first page)
  "results": [...]                // Array of records for current page
}
```

Default page size: **10 records per page**

Navigate using the `page` query parameter:
- `/api/expenses/?page=1` - First page
- `/api/expenses/?page=2` - Second page
- etc. 