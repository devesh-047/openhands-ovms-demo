def test_transaction_history_returns_expected_transactions(client):
    client.post(
        "/register",
        json={"name": "Alice", "email": "alice@example.com", "password": "secret"},
    )
    client.post("/payments", json={"email": "alice@example.com", "amount": 100.0, "description": "Lunch"})
    client.post("/payments", json={"email": "alice@example.com", "amount": 50.0, "description": "Taxi"})

    response = client.get("/transactions", params={"email": "alice@example.com"})

    assert response.status_code == 200
    body = response.json()
    assert body["email"] == "alice@example.com"
    assert len(body["transactions"]) == 2
    assert body["transactions"][0]["amount"] == 100.0
    assert body["transactions"][0]["type"] == "payment"
    assert body["transactions"][0]["description"] == "Lunch"
    assert body["transactions"][1]["amount"] == 50.0
    assert body["transactions"][1]["description"] == "Taxi"


def test_user_with_no_transactions_receives_empty_list(client):
    client.post(
        "/register",
        json={"name": "Alice", "email": "alice@example.com", "password": "secret"},
    )

    response = client.get("/transactions", params={"email": "alice@example.com"})

    assert response.status_code == 200
    assert response.json()["transactions"] == []
