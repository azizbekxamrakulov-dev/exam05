from sqlalchemy import Column, Integer, String, Float
from app.db.base import Base


class Book(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    author = Column(String)
    genre = Column(String)
    year = Column(Integer)
    rating = Column(Float)