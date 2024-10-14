# Narrify User Service

The Narrify User Service is an API built with FastAPI that provides user management and authentication functionalities. This service manages user information, including roles and permissions, enabling a secure way to access and control user-specific operations.

## Features

- **User Registration**: Create new user accounts.
- **User Authentication**: Secure login and password hashing.
- **Role-Based Authorization**: Only authorized roles can access specific endpoints.
- **User Management**: Admins can view, update, and delete user accounts.
- **JWT Authentication**: Tokens are used for securing endpoints and maintaining sessions.

## Requirements

- **Python**: 3.10
- **FastAPI**: Web framework for building APIs.
- **SQLAlchemy**: ORM for database management.
- **PostgreSQL**: Database for storing user data.
- **Docker**: Containerization of the app.

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/your-repo/narrify-user-service.git
   cd narrify-user-service
   ```

2. Set up a virtual environment:
   ```bash
   python3.10 -m venv .venv
   source .venv/bin/activate
   ```

3. Install the dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Set up your `.env` file with the following configuration:
   ```bash
   SECRET_KEY=your_secret_key
   ALGORITHM=HS256
   ACCESS_TOKEN_EXPIRE_MINUTES=30
   DATABASE_URL=postgresql://user:password@localhost:5432/narrify_db
   ```

5. Start the PostgreSQL database:
   ```bash
   docker-compose up -d
   ```

## Running the Application

To run the application locally:

```bash
uvicorn app.main:app --host 0.0.0.0 --port 9000
```

Or with Docker:

1. Build the Docker image:
   ```bash
   docker build -t narrify-user-service .
   ```

2. Run the container:
   ```bash
   docker run -p 9000:9000 narrify-user-service
   ```

## API Endpoints

### Auth

- `POST /token`: Authenticates the user and returns a JWT token.

### Users

- `GET /users/me`: Get the current logged-in user's information.
- `GET /users/{user_id}`: Get user details by ID. (Admin only)
- `GET /users`: Get a list of users. (Admin only)
- `POST /users`: Register a new user.
- `PUT /users/{user_id}`: Update user information. (Admin only)
- `DELETE /users/{user_id}`: Delete a user by ID. (Admin only)

## Role-Based Access

The application includes role-based access control, ensuring that only users with the "admin" role can access certain endpoints. Other endpoints are available for authenticated users.

## Authentication and Security

- **Password Hashing**: Passwords are hashed using `bcrypt`.
- **JWT Tokens**: JSON Web Tokens are used for session management.
- **OAuth2**: The application uses OAuth2 for secure user authentication.

## Project Structure
```
narrify-user-service/
├── app/
│   ├── api/
│   │   └── auth.py           # Authentication API
│   ├── core/
│   │   └── auth.py           # Authentication utilities
│   │   └── config.py         # Configuration settings
│   ├── crud/
│   │   └── user_crud.py      # CRUD operations for users
│   ├── db/
│   │   └── database.py       # Database connection
│   ├── main.py               # FastAPI app entry point
│   └── models/
│       └── user.py           # User model definition
│   └── schemas/
│       └── user_schema.py    # Pydantic schemas for user data
├── .env                      # Environment variables
├── Dockerfile                # Docker configuration
├── requirements.txt          # Python dependencies
└── README.md                 # Project README
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.