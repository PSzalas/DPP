import pytest
from models import Rating

def test_get_ratings_list(client, db):
    db.add(Rating(userId=1, movieId=1, rating=4.0, timestamp=1000))
    db.add(Rating(userId=1, movieId=2, rating=5.0, timestamp=2000))
    db.commit()

    response = client.get("/ratings")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2

def test_get_rating_by_id(client, db):
    db.add(Rating(userId=1, movieId=1, rating=4.0, timestamp=1000))
    db.commit()

    response = client.get("/ratings/1/1")
    assert response.status_code == 200
    data = response.json()
    assert data["userId"] == 1
    assert data["movieId"] == 1
    assert data["rating"] == 4.0

def test_get_rating_not_found(client):
    """
    c. GET item – brak elementu → 404
    """
    response = client.get("/ratings/999/999")
    assert response.status_code == 404

def test_create_rating(client):
    response = client.post("/ratings", json={
        "userId": 10,
        "movieId": 10,
        "rating": 3.5,
        "timestamp": 3000
    })
    assert response.status_code == 201

    r2 = client.get("/ratings/10/10")
    assert r2.status_code == 200
    data = r2.json()
    assert data["rating"] == 3.5

def test_update_rating(client, db):
    db.add(Rating(userId=1, movieId=1, rating=4.0, timestamp=1000))
    db.commit()

    response = client.put("/ratings/1/1", json={"rating": 4.5})
    assert response.status_code == 200

    r2 = client.get("/ratings/1/1")
    data = r2.json()
    assert data["rating"] == 4.5

def test_delete_rating(client, db):
    db.add(Rating(userId=1, movieId=1, rating=4.0, timestamp=1000))
    db.commit()

    response = client.delete("/ratings/1/1")
    assert response.status_code == 200

    r2 = client.get("/ratings/1/1")
    assert r2.status_code == 404
