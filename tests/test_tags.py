import pytest
from models import Tag

def test_get_tags_list(client, db):
    db.add(Tag(userId=1, movieId=1, tag="funny", timestamp=1000))
    db.add(Tag(userId=1, movieId=2, tag="scary", timestamp=2000))
    db.commit()

    response = client.get("/tags")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2

def test_get_tag_by_id(client, db):
    tag = Tag(userId=1, movieId=1, tag="funny", timestamp=1000)
    db.add(tag)
    db.commit()
    tag_id = tag.id

    response = client.get(f"/tags/{tag_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["tag"] == "funny"

def test_get_tag_not_found(client):
    """
    c. GET item – brak elementu → 404
    """
    response = client.get("/tags/999")
    assert response.status_code == 404

def test_create_tag(client):
    response = client.post("/tags", json={
        "userId": 10,
        "movieId": 10,
        "tag": "classic",
        "timestamp": 3000
    })
    assert response.status_code == 201

    r2 = client.get("/tags")
    data = r2.json()
    found = False
    for t in data:
        if t["tag"] == "classic":
            found = True
            break
    assert found

def test_update_tag(client, db):
    tag = Tag(userId=1, movieId=1, tag="funny", timestamp=1000)
    db.add(tag)
    db.commit()
    tag_id = tag.id

    response = client.put(f"/tags/{tag_id}", json={"tag": "hilarious"})
    assert response.status_code == 200

    r2 = client.get(f"/tags/{tag_id}")
    data = r2.json()
    assert data["tag"] == "hilarious"

def test_delete_tag(client, db):
    tag = Tag(userId=1, movieId=1, tag="funny", timestamp=1000)
    db.add(tag)
    db.commit()
    tag_id = tag.id

    response = client.delete(f"/tags/{tag_id}")
    assert response.status_code == 200

    r2 = client.get(f"/tags/{tag_id}")
    assert r2.status_code == 404
