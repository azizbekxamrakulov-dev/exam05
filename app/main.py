from fastapi import FastAPI
from app.db.session import engine
from app.db.base import Base
from app.api.book import router as book_router

app = FastAPI()

Base.metadata.create_all(bind=engine)

app.include_router(book_router)