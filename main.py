from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal, init_db
from models import Movie, Link, Tag, Rating

app = FastAPI()
init_db()

@app.get("/")
def read_root():
    return {"hello": "world"}

def get_db():
    db = SessionLocal()
    print(db.query(Movie).count())
    try:
        yield db
    finally:
        db.close()

# CREATE
@app.post("/movies", status_code=201)
def create_movie(movie: dict, db: Session = Depends(get_db)):
    new_movie = Movie(
        movieId=movie["movieId"],
        title=movie["title"],
        genres=movie["genres"]
    )
    db.add(new_movie)
    db.commit()
    return {"message": "Movie created"}

# READ ALL
@app.get("/movies")
def get_movies(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    movies = db.query(Movie).offset(skip).limit(limit).all()
    return movies

# READ ONE
@app.get("/movies/{movie_id}")
def get_movie(movie_id: int, db: Session = Depends(get_db)):
    movie = db.query(Movie).filter(Movie.movieId == movie_id).first()
    if not movie:
        raise HTTPException(404, "Movie not found")
    return {
        "movieId": movie.movieId,
        "title": movie.title,
        "genres": movie.genres
    }

# UPDATE
@app.put("/movies/{movie_id}")
def update_movie(movie_id: int, data: dict, db: Session = Depends(get_db)):
    movie = db.query(Movie).filter(Movie.movieId == movie_id).first()
    if not movie:
        raise HTTPException(404, "Movie not found")

    movie.title = data.get("title", movie.title)
    movie.genres = data.get("genres", movie.genres)

    db.commit()
    return {"message": "Movie updated"}

# DELETE
@app.delete("/movies/{movie_id}")
def delete_movie(movie_id: int, db: Session = Depends(get_db)):
    movie = db.query(Movie).filter(Movie.movieId == movie_id).first()
    if not movie:
        raise HTTPException(404, "Movie not found")

    db.delete(movie)
    db.commit()
    return {"message": "Movie deleted"}

# CREATE
@app.post("/links", status_code=201)
def create_link(link: dict, db: Session = Depends(get_db)):
    new_link = Link(
        movieId=link["movieId"],
        imdbId=link.get("imdbId"),
        tmdbId=link.get("tmdbId")
    )
    db.add(new_link)
    db.commit()
    return {"message": "Link created"}

# READ ALL
@app.get("/links")
def get_links(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    links = db.query(Link).offset(skip).limit(limit).all()
    return links

# READ ONE
@app.get("/links/{movie_id}")
def get_link(movie_id: int, db: Session = Depends(get_db)):
    link = db.query(Link).filter(Link.movieId == movie_id).first()
    if not link:
        raise HTTPException(404, "Link not found")

    return {
        "movieId": link.movieId,
        "imdbId": link.imdbId,
        "tmdbId": link.tmdbId
    }

# UPDATE
@app.put("/links/{movie_id}")
def update_link(movie_id: int, data: dict, db: Session = Depends(get_db)):
    link = db.query(Link).filter(Link.movieId == movie_id).first()
    if not link:
        raise HTTPException(404, "Link not found")

    link.imdbId = data.get("imdbId", link.imdbId)
    link.tmdbId = data.get("tmdbId", link.tmdbId)

    db.commit()
    return {"message": "Link updated"}

# DELETE
@app.delete("/links/{movie_id}")
def delete_link(movie_id: int, db: Session = Depends(get_db)):
    link = db.query(Link).filter(Link.movieId == movie_id).first()
    if not link:
        raise HTTPException(404, "Link not found")

    db.delete(link)
    db.commit()
    return {"message": "Link deleted"}

# CREATE
@app.post("/ratings", status_code=201)
def create_rating(rating: dict, db: Session = Depends(get_db)):
    new_rating = Rating(
        userId=rating["userId"],
        movieId=rating["movieId"],
        rating=rating["rating"],
        timestamp=rating["timestamp"]
    )
    db.add(new_rating)
    db.commit()
    return {"message": "Rating created"}

# READ ALL
@app.get("/ratings")
def get_ratings(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    ratings = db.query(Rating).offset(skip).limit(limit).all()
    return ratings

# READ ONE
@app.get("/ratings/{user_id}/{movie_id}")
def get_rating(user_id: int, movie_id: int, db: Session = Depends(get_db)):
    rating = db.query(Rating).filter(
        Rating.userId == user_id,
        Rating.movieId == movie_id
    ).first()
    if not rating:
        raise HTTPException(404, "Rating not found")

    return {
        "userId": rating.userId,
        "movieId": rating.movieId,
        "rating": rating.rating,
        "timestamp": rating.timestamp
    }

# UPDATE
@app.put("/ratings/{user_id}/{movie_id}")
def update_rating(user_id: int, movie_id: int, data: dict, db: Session = Depends(get_db)):
    rating = db.query(Rating).filter(
        Rating.userId == user_id,
        Rating.movieId == movie_id
    ).first()

    if not rating:
        raise HTTPException(404, "Rating not found")

    rating.rating = data.get("rating", rating.rating)
    rating.timestamp = data.get("timestamp", rating.timestamp)
    db.commit()

    return {"message": "Rating updated"}

# DELETE
@app.delete("/ratings/{user_id}/{movie_id}")
def delete_rating(user_id: int, movie_id: int, db: Session = Depends(get_db)):
    rating = db.query(Rating).filter(
        Rating.userId == user_id,
        Rating.movieId == movie_id
    ).first()

    if not rating:
        raise HTTPException(404, "Rating not found")

    db.delete(rating)
    db.commit()
    return {"message": "Rating deleted"}

# CREATE
@app.post("/tags", status_code=201)
def create_tag(tag: dict, db: Session = Depends(get_db)):
    new_tag = Tag(
        userId=tag["userId"],
        movieId=tag["movieId"],
        tag=tag["tag"],
        timestamp=tag["timestamp"]
    )
    db.add(new_tag)
    db.commit()
    return {"message": "Tag created"}

# READ ALL
@app.get("/tags")
def get_tags(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    tags = db.query(Tag).offset(skip).limit(limit).all()
    return tags

# READ ONE
@app.get("/tags/{tag_id}")
def get_tag(tag_id: int, db: Session = Depends(get_db)):
    tag = db.query(Tag).filter(Tag.id == tag_id).first()
    if not tag:
        raise HTTPException(404, "Tag not found")

    return {
        "id": tag.id,
        "userId": tag.userId,
        "movieId": tag.movieId,
        "tag": tag.tag,
        "timestamp": tag.timestamp
    }

# UPDATE
@app.put("/tags/{tag_id}")
def update_tag(tag_id: int, data: dict, db: Session = Depends(get_db)):
    tag = db.query(Tag).filter(Tag.id == tag_id).first()
    if not tag:
        raise HTTPException(404, "Tag not found")

    tag.tag = data.get("tag", tag.tag)
    tag.timestamp = data.get("timestamp", tag.timestamp)

    db.commit()
    return {"message": "Tag updated"}

# DELETE
@app.delete("/tags/{tag_id}")
def delete_tag(tag_id: int, db: Session = Depends(get_db)):
    tag = db.query(Tag).filter(Tag.id == tag_id).first()
    if not tag:
        raise HTTPException(404, "Tag not found")

    db.delete(tag)
    db.commit()
    return {"message": "Tag deleted"}

@app.get("/debug")
def debug(db: Session = Depends(get_db)):
    return {
        "movies": db.query(Movie).count(),
        "links": db.query(Link).count(),
        "ratings": db.query(Rating).count(),
        "tags": db.query(Tag).count()
    }
