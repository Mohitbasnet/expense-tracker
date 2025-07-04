# Django Expense Tracker API

A REST API for expense/income tracking with JWT authentication, built with Django REST Framework.

## Features

- **User Authentication**: JWT-based authentication with registration, login, and token refresh
- **Access Control**: Regular users can only manage their own records, superusers can access all records
- **Expense/Income Management**: Complete CRUD operations for financial transactions
- **Tax Calculations**: Automatic tax calculation (flat amount or percentage)
- **Pagination**: Paginated API responses for better performance
- **Comprehensive Testing**: Full test coverage for all features

## Technologies Used

- **Backend**: Django 4.2.7 + Django REST Framework 3.14.0
- **Authentication**: JWT (djangorestframework-simplejwt)
- **Database**: SQLite (for development)
- **Python**: 3.8+

## Project Structure

```
expense_tracker/
├── expense_tracker/          # Main project settings
├── authentication/          # User authentication app
├── expenses/               # Expense/Income management app
├── requirements.txt        # Project dependencies
├── manage.py              # Django management script
└── README.md              # This file
```

## Installation & Setup

### 1. Clone the Repository

```bash
git clone <repository-url>
cd VritTechnoLogyAssignment
```

### 2. Create Virtual Environment (Recommended)

**On Windows:**
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
venv\Scripts\activate
```

**On macOS/Linux:**
```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Run Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### 5. Create Superuser (Optional)

```bash
python manage.py createsuperuser
```

### 6. Run Development Server

```bash
python manage.py runserver
```

The API will be available at `http://127.0.0.1:8000/`

### 7. Deactivate Virtual Environment (When Done)

```bash
deactivate
```

## API Endpoints

### Authentication Endpoints

| Method | URL | Description |
|--------|-----|-------------|
| POST | `/api/auth/register/` | User registration |
| POST | `/api/auth/login/` | User login |
| POST | `/api/auth/refresh/` | Refresh JWT token |

### Expense/Income Endpoints

| Method | URL | Description |
|--------|-----|-------------|
| GET | `/api/expenses/` | List user's records (paginated) |
| POST | `/api/expenses/` | Create new record |
| GET | `/api/expenses/{id}/` | Get specific record |
| PUT | `/api/expenses/{id}/` | Update record |
| PATCH | `/api/expenses/{id}/` | Partial update record |
| DELETE | `/api/expenses/{id}/` | Delete record |

## API Usage Examples

### 1. User Registration

```bash
curl -X POST http://127.0.0.1:8000/api/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "johndoe",
    "email": "john@example.com",
    "first_name": "John",
    "last_name": "Doe",
    "password": "securepass123",
    "password_confirm": "securepass123"
  }'
```

**Response:**
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

### 2. User Login

```bash
curl -X POST http://127.0.0.1:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "johndoe",
    "password": "securepass123"
  }'
```

### 3. Create Expense/Income Record

```bash
curl -X POST http://127.0.0.1:8000/api/expenses/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -d '{
    "title": "Grocery Shopping",
    "description": "Weekly groceries",
    "amount": "100.00",
    "transaction_type": "debit",
    "tax": "10.00",
    "tax_type": "flat"
  }'
```

**Response:**
```json
{
  "id": 1,
  "title": "Grocery Shopping",
  "description": "Weekly groceries",
  "amount": "100.00",
  "transaction_type": "debit",
  "tax": "10.00",
  "tax_type": "flat",
  "total": "110.00",
  "created_at": "2025-01-01T10:00:00Z",
  "updated_at": "2025-01-01T10:00:00Z"
}
```

### 4. List Expenses/Income Records

```bash
curl -X GET http://127.0.0.1:8000/api/expenses/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

**Response:**
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
    }
  ]
}
```

## Database Models

### ExpenseIncome Model

| Field | Type | Description |
|-------|------|-------------|
| `user` | ForeignKey | Reference to User model |
| `title` | CharField(200) | Title of the transaction |
| `description` | TextField | Optional description |
| `amount` | DecimalField | Transaction amount |
| `transaction_type` | CharField | 'credit' or 'debit' |
| `tax` | DecimalField | Tax amount (default: 0) |
| `tax_type` | CharField | 'flat' or 'percentage' (default: 'flat') |
| `created_at` | DateTimeField | Auto-generated creation time |
| `updated_at` | DateTimeField | Auto-generated update time |

### Business Logic

- **Flat Tax**: Total = Amount + Tax
- **Percentage Tax**: Total = Amount + (Amount × Tax ÷ 100)

## Authentication & Permissions

- **JWT Tokens**: All API endpoints require valid JWT access tokens
- **User Isolation**: Regular users can only access their own records
- **Superuser Access**: Superusers can access and manage all users' records
- **Token Refresh**: Use refresh tokens to get new access tokens

## HTTP Status Codes

| Code | Description |
|------|-------------|
| 200 | OK - Successful GET, PUT |
| 201 | Created - Successful POST |
| 204 | No Content - Successful DELETE |
| 400 | Bad Request - Invalid data |
| 401 | Unauthorized - Authentication required |
| 403 | Forbidden - Permission denied |
| 404 | Not Found - Resource not found |

## Testing

### Run All Tests

```bash
python manage.py test
```

### Run Specific Test Module

```bash
# Test authentication
python manage.py test authentication

# Test expenses
python manage.py test expenses
```

### Test Coverage

The project includes comprehensive tests for:

- **Authentication Tests**
  - User registration (success, duplicate email, password mismatch)
  - User login (success, invalid credentials)
  - JWT token functionality
  - Protected endpoint access

- **CRUD Operations Tests**
  - Create, read, update, delete expense/income records
  - User permission isolation
  - Superuser access verification

- **Business Logic Tests**
  - Flat tax calculations
  - Percentage tax calculations
  - Zero tax scenarios

- **Permission Tests**
  - Regular user access restrictions
  - Superuser privileges
  - Unauthenticated request rejection

## API Testing with Postman

### 1. Import Environment Variables

Create a Postman environment with:
- `base_url`: `http://127.0.0.1:8000`
- `access_token`: (will be set after login)

### 2. Authentication Flow

1. Register a new user
2. Login to get tokens
3. Set `access_token` in environment
4. Use `{{access_token}}` in Authorization headers

### 3. Sample Requests Collection

Import or create these requests in Postman:

```
POST {{base_url}}/api/auth/register/
POST {{base_url}}/api/auth/login/
POST {{base_url}}/api/auth/refresh/
GET {{base_url}}/api/expenses/
POST {{base_url}}/api/expenses/
GET {{base_url}}/api/expenses/1/
PUT {{base_url}}/api/expenses/1/
DELETE {{base_url}}/api/expenses/1/
```

## Development

### Creating Migrations

```bash
python manage.py makemigrations
```

### Applying Migrations

```bash
python manage.py migrate
```

### Django Admin

Access the Django admin at `http://127.0.0.1:8000/admin/` with superuser credentials.

### Adding New Features

1. Create models in appropriate app
2. Create serializers for data validation
3. Create views/viewsets with proper permissions
4. Add URL routing
5. Write comprehensive tests
6. Update documentation

## Production Deployment

For production deployment:

1. Set `DEBUG = False` in settings
2. Configure proper database (PostgreSQL recommended)
3. Set up environment variables for sensitive data
4. Configure static file serving
5. Set up proper CORS settings
6. Use HTTPS for JWT token security
7. Configure proper logging

## Contributing

1. Fork the repository
2. Create a feature branch
3. Write tests for new features
4. Ensure all tests pass
5. Submit a pull request

## License

This project is licensed under the MIT License. 