from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import declarative_base
from pydantic import BaseModel

Base = declarative_base()

class Movie(Base):
    __tablename__ = "movies"
    movieId = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    genres = Column(String)

class Link(Base):
    __tablename__ = "links"
    movieId = Column(Integer, primary_key=True)
    imdbId = Column(String)
    tmdbId = Column(Integer, nullable=True)

class Rating(Base):
    __tablename__ = "ratings"
    userId = Column(Integer, primary_key=True)
    movieId = Column(Integer, primary_key=True)
    rating = Column(Float)
    timestamp = Column(Integer)

class Tag(Base):
    __tablename__ = "tags"
    id = Column(Integer, primary_key=True, autoincrement=True)
    userId = Column(Integer)
    movieId = Column(Integer)
    tag = Column(String)
    timestamp = Column(Integer)

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    password_hash = Column(String)
    roles = Column(String) # Comma-separated roles, e.g., "ROLE_USER,ROLE_ADMIN"

class UserCreate(BaseModel):
    username: str
    password: str
    roles: str = "ROLE_USER"