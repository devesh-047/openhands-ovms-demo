def test_normal_positive_payment_succeeds(client):
    client.post(
        "/register",
        json={"name": "Alice", "email": "alice@example.com", "password": "secret"},
    )

    response = client.post(
        "/payments",
        json={"email": "alice@example.com", "amount": 125.5, "description": "Groceries"},
    )

    assert response.status_code == 200
    body = response.json()
    assert body["message"] == "Payment successful"
    assert body["balance"] == 874.5


def test_payment_larger_than_balance_is_rejected(client):
    client.post(
        "/register",
        json={"name": "Alice", "email": "alice@example.com", "password": "secret"},
    )

    response = client.post(
        "/payments",
        json={"email": "alice@example.com", "amount": 2000.0},
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "Insufficient balance"


def test_successful_payment_decreases_balance(client):
    client.post(
        "/register",
        json={"name": "Alice", "email": "alice@example.com", "password": "secret"},
    )

    client.post("/payments", json={"email": "alice@example.com", "amount": 100.0})
    response = client.post("/payments", json={"email": "alice@example.com", "amount": 50.0})

    assert response.status_code == 200
    assert response.json()["balance"] == 850.0


def test_successful_payment_creates_transaction(client):
    client.post(
        "/register",
        json={"name": "Alice", "email": "alice@example.com", "password": "secret"},
    )

    response = client.post(
        "/payments",
        json={"email": "alice@example.com", "amount": 25.0, "description": "Coffee"},
    )

    assert response.status_code == 200
    transaction_id = response.json()["transaction_id"]

    history_response = client.get("/transactions", params={"email": "alice@example.com"})
    transactions = history_response.json()["transactions"]

    assert len(transactions) == 1
    assert transactions[0]["id"] == transaction_id
    assert transactions[0]["amount"] == 25.0
    assert transactions[0]["description"] == "Coffee"
