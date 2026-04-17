from pydantic import BaseModel


class BookBase(BaseModel):
    title: str
    author: str
    genre: str
    year: int
    rating: float


class BookCreate(BookBase):
    pass


class BookUpdate(BookBase):
    pass


class BookResponse(BookBase):
    id: int

    class Config:
        from_attributes = True