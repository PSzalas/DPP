import pytest
from models import Movie

def test_get_movies_list(client, db):
    """
    a. GET lista – czy zwraca tyle elementów ile w fixturze?
    """
    db.add_all([
        db.query(Movie).filter(Movie.movieId==1).first() or Movie(movieId=1, title="Movie A", genres="Action"),
        db.query(Movie).filter(Movie.movieId==2).first() or Movie(movieId=2, title="Movie B", genres="Comedy"),
    ])
    db.commit()

    response = client.get("/movies")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    assert data[0]["movieId"] == 1
    assert data[1]["movieId"] == 2


def test_get_movie_by_id(client, db):
    """
    b. GET item – czy zwraca poprawny element?
    """
    db.add(Movie(movieId=1, title="Movie A", genres="Action"))
    db.commit()

    response = client.get("/movies/1")
    assert response.status_code == 200
    movie = response.json()
    assert movie["movieId"] == 1
    assert movie["title"] == "Movie A"
    assert movie["genres"] == "Action"


def test_get_movie_not_found(client):
    """
    c. GET item – brak elementu → 404
    """
    response = client.get("/movies/999")
    assert response.status_code == 404


def test_create_movie(client):
    """
    d. POST – czy dodaje element do bazy?
    """
    response = client.post("/movies", json={
        "movieId": 10,
        "title": "New Movie",
        "genres": "Drama"
    })
    assert response.status_code == 201

    r2 = client.get("/movies/10")
    assert r2.status_code == 200
    data = r2.json()
    assert data["title"] == "New Movie"
    assert data["genres"] == "Drama"


def test_update_movie(client, db):
    """
    e. PUT – czy zmiana zapisuje się w bazie?
    """
    db.add(Movie(movieId=1, title="Old Title", genres="Action"))
    db.commit()

    response = client.put("/movies/1", json={"title": "Updated Title"})
    assert response.status_code == 200

    r2 = client.get("/movies/1")
    data = r2.json()
    assert data["title"] == "Updated Title"


def test_delete_movie(client, db):
    """
    f. DELETE – czy element został usunięty?
    """
    db.add(Movie(movieId=1, title="To Delete", genres="Action"))
    db.commit()

    response = client.delete("/movies/1")
    assert response.status_code == 200

    r2 = client.get("/movies/1")
    assert r2.status_code == 404