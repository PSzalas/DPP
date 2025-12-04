from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import init_db, get_db
from models import Movie, Link, Tag, Rating, User, UserCreate
from pydantic import BaseModel
from datetime import datetime, timedelta
import auth
from auth import get_current_user, get_current_admin_user
from fastapi.security import OAuth2PasswordRequestForm

app = FastAPI()
init_db()

@app.get("/")
def read_root():
    return {"hello": "world"}

# LOGIN
@app.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == form_data.username).first()
    if not user or not auth.verify_password(form_data.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=auth.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = auth.create_access_token(
        data={"sub": user.username, "roles": user.roles}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

# CREATE USER
@app.post("/users", status_code=201)
def create_user(user: UserCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_admin_user)):
    db_user = db.query(User).filter(User.username == user.username).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    hashed_password = auth.get_password_hash(user.password)
    new_user = User(username=user.username, password_hash=hashed_password, roles=user.roles)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"username": new_user.username, "roles": new_user.roles}

# USER DETAILS
@app.get("/user_details")
def read_users_me(current_user: User = Depends(get_current_user)):
    return {"username": current_user.username, "roles": current_user.roles}

# CREATE
@app.post("/movies", status_code=201)
def create_movie(movie: dict, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
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
def get_movies(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    movies = db.query(Movie).offset(skip).limit(limit).all()
    return movies

# READ ONE
@app.get("/movies/{movie_id}")
def get_movie(movie_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
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
def update_movie(movie_id: int, data: dict, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    movie = db.query(Movie).filter(Movie.movieId == movie_id).first()
    if not movie:
        raise HTTPException(404, "Movie not found")

    movie.title = data.get("title", movie.title)
    movie.genres = data.get("genres", movie.genres)

    db.commit()
    return {"message": "Movie updated"}

# DELETE
@app.delete("/movies/{movie_id}")
def delete_movie(movie_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    movie = db.query(Movie).filter(Movie.movieId == movie_id).first()
    if not movie:
        raise HTTPException(404, "Movie not found")

    db.delete(movie)
    db.commit()
    return {"message": "Movie deleted"}

# CREATE
@app.post("/links", status_code=201)
def create_link(link: dict, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
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
def get_links(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    links = db.query(Link).offset(skip).limit(limit).all()
    return links

# READ ONE
@app.get("/links/{movie_id}")
def get_link(movie_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
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
def update_link(movie_id: int, data: dict, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    link = db.query(Link).filter(Link.movieId == movie_id).first()
    if not link:
        raise HTTPException(404, "Link not found")

    link.imdbId = data.get("imdbId", link.imdbId)
    link.tmdbId = data.get("tmdbId", link.tmdbId)

    db.commit()
    return {"message": "Link updated"}

# DELETE
@app.delete("/links/{movie_id}")
def delete_link(movie_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    link = db.query(Link).filter(Link.movieId == movie_id).first()
    if not link:
        raise HTTPException(404, "Link not found")

    db.delete(link)
    db.commit()
    return {"message": "Link deleted"}

# CREATE
@app.post("/ratings", status_code=201)
def create_rating(rating: dict, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
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
def get_ratings(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    ratings = db.query(Rating).offset(skip).limit(limit).all()
    return ratings

# READ ONE
@app.get("/ratings/{user_id}/{movie_id}")
def get_rating(user_id: int, movie_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
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
def update_rating(user_id: int, movie_id: int, data: dict, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
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
def delete_rating(user_id: int, movie_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
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
def create_tag(tag: dict, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
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
def get_tags(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    tags = db.query(Tag).offset(skip).limit(limit).all()
    return tags

# READ ONE
@app.get("/tags/{tag_id}")
def get_tag(tag_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
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
def update_tag(tag_id: int, data: dict, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    tag = db.query(Tag).filter(Tag.id == tag_id).first()
    if not tag:
        raise HTTPException(404, "Tag not found")

    tag.tag = data.get("tag", tag.tag)
    tag.timestamp = data.get("timestamp", tag.timestamp)

    db.commit()
    return {"message": "Tag updated"}

# DELETE
@app.delete("/tags/{tag_id}")
def delete_tag(tag_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    tag = db.query(Tag).filter(Tag.id == tag_id).first()
    if not tag:
        raise HTTPException(404, "Tag not found")

    db.delete(tag)
    db.commit()
    return {"message": "Tag deleted"}

@app.get("/debug")
def debug(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return {
        "movies": db.query(Movie).count(),
        "links": db.query(Link).count(),
        "ratings": db.query(Rating).count(),
        "tags": db.query(Tag).count()
    }
