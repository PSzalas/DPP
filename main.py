from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from database import SessionLocal, init_db
from models import Movie, Link, Tag, Rating

app = FastAPI()
init_db()

def get_db():
    db = SessionLocal()
    print(db.query(Movie).count())
    try:
        yield db
    finally:
        db.close()

@app.get("/movies")
def get_movies(db: Session = Depends(get_db)):
    movies = db.query(Movie).all()
    return [{"movieId": m.movieId, "title": m.title, "genres": m.genres} for m in movies]

@app.get("/links")
def get_links(db: Session = Depends(get_db)):
    links = db.query(Link).all()
    return [
        {
            "movieId": l.movieId,
            "imdbId": l.imdbId,
            "tmdbId": l.tmdbId
        }
        for l in links
    ]


@app.get("/ratings")
def get_ratings(db: Session = Depends(get_db)):
    ratings = db.query(Rating).all()
    return [
        {
            "userId": r.userId,
            "movieId": r.movieId,
            "rating": r.rating,
            "timestamp": r.timestamp
        }
        for r in ratings
    ]


@app.get("/tags")
def get_tags(db: Session = Depends(get_db)):
    tags = db.query(Tag).all()
    return [
        {
            "id": t.id,
            "userId": t.userId,
            "movieId": t.movieId,
            "tag": t.tag,
            "timestamp": t.timestamp
        }
        for t in tags
    ]

@app.get("/debug")
def debug(db: Session = Depends(get_db)):
    return {
        "movies": db.query(Movie).count(),
        "links": db.query(Link).count(),
        "ratings": db.query(Rating).count(),
        "tags": db.query(Tag).count()
    }
