import pytest
from auth import get_password_hash
from models import User

def test_login_success(client, db):
    # Create user
    hashed_password = get_password_hash("testpassword")
    user = User(username="testuser", password_hash=hashed_password, roles="ROLE_USER")
    db.add(user)
    db.commit()

    response = client.post("/login", data={"username": "testuser", "password": "testpassword"})
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"

def test_login_failure(client):
    response = client.post("/login", data={"username": "wronguser", "password": "wrongpassword"})
    assert response.status_code == 401

def test_create_user_as_admin(client, db):
    # Create admin user
    hashed_password = get_password_hash("adminpass")
    admin = User(username="admin", password_hash=hashed_password, roles="ROLE_ADMIN")
    db.add(admin)
    db.commit()

    # Login as admin
    login_res = client.post("/login", data={"username": "admin", "password": "adminpass"})
    token = login_res.json()["access_token"]

    # Create new user
    response = client.post(
        "/users",
        json={"username": "newuser", "password": "newpassword", "roles": "ROLE_USER"},
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 201
    assert response.json()["username"] == "newuser"

    # Verify user in DB
    user = db.query(User).filter(User.username == "newuser").first()
    assert user is not None

def test_create_user_as_non_admin(client, db):
    # Create regular user
    hashed_password = get_password_hash("userpass")
    user = User(username="user", password_hash=hashed_password, roles="ROLE_USER")
    db.add(user)
    db.commit()

    # Login as user
    login_res = client.post("/login", data={"username": "user", "password": "userpass"})
    token = login_res.json()["access_token"]

    # Try to create new user
    response = client.post(
        "/users",
        json={"username": "anotheruser", "password": "password", "roles": "ROLE_USER"},
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 403

def test_user_details(client, db):
    # Create user
    hashed_password = get_password_hash("testpass")
    user = User(username="testuser", password_hash=hashed_password, roles="ROLE_USER")
    db.add(user)
    db.commit()

    # Login
    login_res = client.post("/login", data={"username": "testuser", "password": "testpass"})
    token = login_res.json()["access_token"]

    # Get details
    response = client.get("/user_details", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    assert response.json()["username"] == "testuser"

def test_user_details_no_token(client):
    response = client.get("/user_details")
    assert response.status_code == 401

def test_protected_endpoint_access(client, db):
    # Create user
    hashed_password = get_password_hash("testpass")
    user = User(username="testuser", password_hash=hashed_password, roles="ROLE_USER")
    db.add(user)
    db.commit()

    # Login
    login_res = client.post("/login", data={"username": "testuser", "password": "testpass"})
    token = login_res.json()["access_token"]

    # Access protected endpoint (e.g., /movies)
    response = client.get("/movies", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200

def test_protected_endpoint_no_token(client):
    response = client.get("/movies")
    assert response.status_code == 401
