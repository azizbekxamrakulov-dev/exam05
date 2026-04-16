from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List
from .. import models, schemas, database

router = APIRouter(prefix="/books", tags=["Books"])

# Barcha kitoblarni olish
@router.get("/", response_model=List[schemas.BookResponse])
def get_books(db: Session = Depends(database.get_db)):
    return db.query(models.Book).all()

# ID orqali bitta kitobni olish
@router.get("/{book_id}", response_model=schemas.BookResponse)
def get_book(book_id: int, db: Session = Depends(database.get_db)):
    book = db.query(models.Book).filter(models.Book.id == book_id).first()
    if not book:
        raise HTTPException(status_code=404, detail="Kitob topilmadi")
    return book

# Yangi kitob yaratish
@router.post("/", response_model=schemas.BookResponse)
def create_book(book: schemas.BookCreate, db: Session = Depends(database.get_db)):
    new_book = models.Book(**book.model_dump())
    db.add(new_book)
    db.commit()
    db.refresh(new_book)
    return new_book

# Kitobni tahrirlash
@router.put("/{book_id}", response_model=schemas.BookResponse)
def update_book(book_id: int, updated_book: schemas.BookCreate, db: Session = Depends(database.get_db)):
    book_query = db.query(models.Book).filter(models.Book.id == book_id)
    if not book_query.first():
        raise HTTPException(status_code=404, detail="Kitob topilmadi")
    book_query.update(updated_book.model_dump(), synchronize_session=False)
    db.commit()
    return book_query.first()

# Kitobni o'chirish
@router.delete("/{book_id}")
def delete_book(book_id: int, db: Session = Depends(database.get_db)):
    book = db.query(models.Book).filter(models.Book.id == book_id).first()
    if not book:
        raise HTTPException(status_code=404, detail="Kitob topilmadi")
    db.delete(book)
    db.commit()
    return {"status": "Kitob muvaffaqiyatli o'chirildi"}

# Qidiruv (Title yoki Author bo'yicha)
@router.get("/search/", response_model=List[schemas.BookResponse])
def search_books(search: str, db: Session = Depends(database.get_db)):
    return db.query(models.Book).filter(
        (models.Book.title.ilike(f"%{search}%")) | 
        (models.Book.author.ilike(f"%{search}%"))
    ).all()

# Filtr (Yil oralig'i bo'yicha)
@router.get("/filter/", response_model=List[schemas.BookResponse])
def filter_books(min: int, max: int, db: Session = Depends(database.get_db)):
    return db.query(models.Book).filter(models.Book.year >= min, models.Book.year <= max).all()