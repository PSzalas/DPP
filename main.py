from fastapi import FastAPI
import pandas as pd
from Models.Movie import Movie
from Models.Link import Link
from Models.Rating import Rating
from Models.Tag import Tag

app = FastAPI()

@app.get("/")
def read_root():
    return {"hello": "world"}

@app.get("/movies")
def get_movies():
    df = pd.read_csv("database/movies.csv")
    movies = []
    for _, row in df.iterrows():
        movie = Movie(row["movieId"], row["title"], row["genres"])
        movies.append(movie.__dict__)
    return movies

@app.get("/links")
def get_links():
    df = pd.read_csv("database/links.csv")
    links = []
    for _, row in df.iterrows():
        tmdbId = None if pd.isna(row.get("tmdbId")) else row["tmdbId"]
        link = Link(row["movieId"], row["imdbId"], tmdbId)
        links.append(link.__dict__)
    return links

@app.get("/ratings")
def get_ratings():
    df = pd.read_csv("database/ratings.csv")
    ratings = []
    for _, row in df.iterrows():
        r = Rating(row["userId"], row["movieId"], row["rating"], row["timestamp"])
        ratings.append(r.__dict__)
    return ratings

@app.get("/tags")
def get_tags():
    df = pd.read_csv("database/tags.csv")
    tags = []
    for _, row in df.iterrows():
        t = Tag(row["userId"], row["movieId"], row["tag"], row["timestamp"])
        tags.append(t.__dict__)
    return tags
