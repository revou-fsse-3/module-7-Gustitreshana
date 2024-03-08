# Flask MySQL CRUD Application

This Flask application is a simple CRUD (Create, Read, Update, Delete) web application that allows users to manage products and user accounts. It integrates with a MySQL database for data storage and incorporates session-based and token-based authentication methods using Flask-Login and Flask-JWT-Extended.

## Features

- **User Management**: Users can register, log in, and log out securely. Passwords are hashed using bcrypt for security.
- **Product Management**: Users can perform CRUD operations on products, including creating, reading, updating, and deleting products.
- **Session-Based Authentication**: Flask-Login is used for session-based authentication, allowing users to authenticate with their credentials and access protected routes.
- **Token-Based Authentication**: Flask-JWT-Extended is used for token-based authentication, generating JWT tokens upon successful login, which are then used to access protected routes.
- **Error Handling**: The application includes error handling mechanisms to handle potential errors during database operations or authentication processes.

## Project Structure

The project structure is organized as follows:

- `app/`: Contains the Flask application code.
  - `controllers/`: Contains controllers for user and product routes.
  - `connectors/`: Contains database connector code for MySQL.
  - `models/`: Contains SQLAlchemy models for users and products.
  - `templates/`: Contains HTML templates for rendering web pages.
  - `tests/`: Contains unit tests for the application.
- `.venv/`: Virtual environment for managing dependencies.

## Installation

To run the application locally, follow these steps:

1. Clone the repository: `git clone https://github.com/revou-fsse-3/module-7-Gustitreshana.git`
2. Navigate to the project directory: `cd flask-mysql-crud`
3. Install dependencies using Poetry: `poetry install`
4. Set up environment variables:
   - Create a `.env` file and define the necessary environment variables, such as `SECRET_KEY`, `DATABASE_USERNAME`, `DATABASE_PASSWORD`, `DATABASE_URL`, and `DATABASE_NAME`.
5. Initialize the MySQL database: `poetry run flask db upgrade`
6. Run the Flask application: `poetry run flask --app app run`

## Usage

- Access the application in your web browser at `http://localhost:5000`.
- Register a new user account or log in with existing credentials.
- Manage products by adding, editing, or deleting them.
- Log out of the application when done.

For detailed API documentation, refer to the [API Documentation](https://documenter.getpostman.com/view/29213022/2sA2xh2CXP) created using Postman.

## Dependencies

The application uses the following dependencies:

- Flask
- Flask-Login
- Flask-JWT-Extended
- SQLAlchemy
- MySQL Connector Python
- Bcrypt

## Contributing

Contributions to this project are welcome! If you find any bugs or have suggestions for improvements, please open an issue or submit a pull request.
