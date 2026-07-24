# Demo Banking API

Demo Banking API is a small FastAPI application that exposes a simple in-memory banking workflow for user registration, login, payments, and transaction history.

## Features

- Health check endpoint
- User registration and login
- Payments against an in-memory balance
- Transaction history lookup
- FastAPI Swagger/OpenAPI docs

## Project Structure

- `app/main.py` - FastAPI application setup
- `app/models.py` - Pydantic request and response models
- `app/store.py` - In-memory users, balances, and transactions
- `app/auth.py` - Registration and login routes
- `app/payments.py` - Payment routes
- `app/transactions.py` - Transaction history routes
- `tests/` - pytest suite using FastAPI TestClient

## Installation

```bash
python -m pip install -r requirements.txt
```

## Run the Application

```bash
uvicorn app.main:app --reload
```

## API Documentation

Swagger UI is available at:

- `/docs`

## Run Tests

```bash
pytest -v
```

## Endpoints

- `GET /health` - health check
- `POST /register` - register a user
- `POST /login` - authenticate a user
- `POST /payments` - create a payment
- `GET /transactions?email=...` - fetch transaction history
