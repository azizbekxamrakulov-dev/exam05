from fastapi import FastAPI
from .database import engine, Base
from .routers import books

# Jadvalni avtomatik yaratish
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Book Management API")

# Routerni ulash
app.include_router(books.router)

@app.get("/")
def root():
    return {"message": "Book Management API ishga tushdi!"}