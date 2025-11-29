import sys
import os
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from main import app, get_db
from models import Base, Movie, Link, Rating, Tag

# ---- BAZA TESTOWA ----
TEST_DB_URL = "sqlite:///./test.db"

engine = create_engine(
    TEST_DB_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine
)

# ---- FIXTURE BAZY ----
@pytest.fixture(scope="session", autouse=True)
def setup_database():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)


# ---- FIXTURE SESJI ----
@pytest.fixture()
def db():
    session = TestingSessionLocal()
    yield session
    session.close()


# ---- FIXTURE API ----
@pytest.fixture()
def client(db):
    # nadpisujemy get_db na testową sesję
    def override_get_db():
        try:
            yield db
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db
    return TestClient(app)

@pytest.fixture(autouse=True)
def clear_db(db):
    db.query(Movie).delete()
    db.query(Link).delete()
    db.query(Rating).delete()
    db.query(Tag).delete()
    db.commit()


# ---- FIXTURE DANYCH TESTOWYCH ----
@pytest.fixture()
def sample_movies(db):
    movies = [
        Movie(movieId=1, title="Movie A", genres="Action"),
        Movie(movieId=2, title="Movie B", genres="Comedy"),
    ]
    for m in movies:
        db.add(m)
    db.commit()
    return movies