import pytest
from models import Link

def test_get_links_list(authorized_client, db):
    db.add(Link(movieId=1, imdbId="tt0000001", tmdbId=1))
    db.add(Link(movieId=2, imdbId="tt0000002", tmdbId=2))
    db.commit()

    response = authorized_client.get("/links")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2

def test_get_link_by_id(authorized_client, db):
    db.add(Link(movieId=1, imdbId="tt0000001", tmdbId=1))
    db.commit()

    response = authorized_client.get("/links/1")
    assert response.status_code == 200
    data = response.json()
    assert data["movieId"] == 1
    assert data["imdbId"] == "tt0000001"

def test_get_link_not_found(authorized_client):
    """
    c. GET item – brak elementu → 404
    """
    response = authorized_client.get("/links/999")
    assert response.status_code == 404

def test_create_link(authorized_client):
    response = authorized_client.post("/links", json={
        "movieId": 10,
        "imdbId": "tt0000010",
        "tmdbId": 10
    })
    assert response.status_code == 201

    r2 = authorized_client.get("/links/10")
    assert r2.status_code == 200
    data = r2.json()
    assert data["imdbId"] == "tt0000010"

def test_update_link(authorized_client, db):
    db.add(Link(movieId=1, imdbId="tt0000001", tmdbId=1))
    db.commit()

    response = authorized_client.put("/links/1", json={"imdbId": "tt9999999"})
    assert response.status_code == 200

    r2 = authorized_client.get("/links/1")
    data = r2.json()
    assert data["imdbId"] == "tt9999999"

def test_delete_link(authorized_client, db):
    db.add(Link(movieId=1, imdbId="tt0000001", tmdbId=1))
    db.commit()

    response = authorized_client.delete("/links/1")
    assert response.status_code == 200

    r2 = authorized_client.get("/links/1")
    assert r2.status_code == 404
