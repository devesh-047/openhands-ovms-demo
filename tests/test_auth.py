def test_valid_registration_succeeds(client):
    response = client.post(
        "/register",
        json={"name": "Alice", "email": "alice@example.com", "password": "secret"},
    )

    assert response.status_code == 201
    body = response.json()
    assert body["name"] == "Alice"
    assert body["email"] == "alice@example.com"
    assert body["balance"] == 1000.0


def test_duplicate_email_registration_is_rejected(client):
    client.post(
        "/register",
        json={"name": "Alice", "email": "alice@example.com", "password": "secret"},
    )

    response = client.post(
        "/register",
        json={"name": "Alice Two", "email": "alice@example.com", "password": "secret2"},
    )

    assert response.status_code == 409
    assert response.json()["detail"] == "Email already registered"


def test_valid_login_succeeds(client):
    client.post(
        "/register",
        json={"name": "Alice", "email": "alice@example.com", "password": "secret"},
    )

    response = client.post("/login", json={"email": "alice@example.com", "password": "secret"})

    assert response.status_code == 200
    body = response.json()
    assert body["message"] == "Login successful"
    assert body["user"]["email"] == "alice@example.com"


def test_incorrect_password_is_rejected(client):
    client.post(
        "/register",
        json={"name": "Alice", "email": "alice@example.com", "password": "secret"},
    )

    response = client.post("/login", json={"email": "alice@example.com", "password": "wrong"})

    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid password"


def test_unknown_user_login_is_rejected(client):
    response = client.post("/login", json={"email": "missing@example.com", "password": "secret"})

    assert response.status_code == 404
    assert response.json()["detail"] == "User not found"


def test_invalid_email_is_rejected(client):
    response = client.post(
        "/register",
        json={"name": "Alice", "email": "john@", "password": "secret"},
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "Invalid email"


def test_email_without_domain_is_rejected(client):
    response = client.post(
        "/register",
        json={"name": "Alice", "email": "john@", "password": "secret"},
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "Invalid email"


def test_email_without_tld_is_rejected(client):
    response = client.post(
        "/register",
        json={"name": "Alice", "email": "john@domain", "password": "secret"},
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "Invalid email"
