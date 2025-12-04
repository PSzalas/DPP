import pandas as pd
from sqlalchemy.orm import Session
from models import Movie, Link, Rating, Tag, User
from database import SessionLocal, init_db
from auth import get_password_hash

init_db()
session: Session = SessionLocal()

# movies
df_movies = pd.read_csv("database/movies.csv")
for _, row in df_movies.iterrows():
    movie = Movie(movieId=row["movieId"], title=row["title"], genres=row["genres"])
    session.add(movie)

# links
df_links = pd.read_csv("database/links.csv")

# Jeśli kolumna tmdbId istnieje
if "tmdbId" in df_links.columns:
    df_links["tmdbId"] = pd.to_numeric(df_links["tmdbId"], errors="coerce")
else:
    df_links["tmdbId"] = pd.NA

for _, row in df_links.iterrows():
    link = Link(
        movieId=row["movieId"],
        imdbId=row["imdbId"],
        tmdbId=row["tmdbId"] if not pd.isna(row["tmdbId"]) else None
    )
    session.add(link)

# ratings
df_ratings = pd.read_csv("database/ratings.csv")
for _, row in df_ratings.iterrows():
    rating = Rating(userId=row["userId"], movieId=row["movieId"], rating=row["rating"], timestamp=row["timestamp"])
    session.add(rating)

# tags
df_tags = pd.read_csv("database/tags.csv")
for _, row in df_tags.iterrows():
    tag = Tag(userId=row["userId"], movieId=row["movieId"], tag=row["tag"], timestamp=row["timestamp"])
    session.add(tag)

# users
user = User(username="user1", password_hash=get_password_hash("password"), roles="ROLE_USER")
session.add(user)

admin = User(username="admin1", password_hash=get_password_hash("password"), roles="ROLE_USER,ROLE_ADMIN")
session.add(admin)

session.commit()
session.close()