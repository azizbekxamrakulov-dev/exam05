from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.schemas.book import BookCreate, BookUpdate, BookResponse
from app.services.book_service import BookService
from app.db.session import get_db

router = APIRouter(prefix="/books", tags=["Books"])
service = BookService()


@router.get("/", response_model=List[BookResponse])
def get_books(db: Session = Depends(get_db)):
    """
    Barcha kitoblar ro\'yxatini olish.

    Ushbu endpoint ma'lumotlar bazasida saqlangan barcha kitoblarni
    ro\'yxat ko\'rinishida qaytaradi.
    """
    return service.get_all_books(db)


@router.get("/{book_id}", response_model=BookResponse)
def get_book(book_id: int, db: Session = Depends(get_db)):
    """
    Berilgan ID bo\'yicha bitta kitobni olish.

    Parametrlar:
    book_id (int): olinadigan kitobning ID raqami
    """
    book = service.get_book_by_id(db, book_id)

    if not book:
        raise HTTPException(status_code=404, detail="Kitob topilmadi")

    return book


@router.post("/", response_model=BookResponse)
def create_book(book: BookCreate, db: Session = Depends(get_db)):
    """
    Yangi kitob qo\'shish.

    Foydalanuvchi tomonidan yuborilgan ma'lumotlar asosida
    yangi kitob ma'lumotlar bazasiga saqlanadi.
    """
    return service.create_book(db, book)


@router.put("/{book_id}", response_model=BookResponse)
def update_book(book_id: int, book: BookUpdate, db: Session = Depends(get_db)):
    """
    Mavjud kitob ma'lumotlarini yangilash.

    Parametrlar:
    book_id (int): yangilanadigan kitobning ID raqami
    """
    updated = service.update_book(db, book_id, book)

    if not updated:
        raise HTTPException(status_code=404, detail="Kitob topilmadi")

    return updated


@router.delete("/{book_id}")
def delete_book(book_id: int, db: Session = Depends(get_db)):
    """
    Kitobni o\'chirish.

    Parametrlar:
    book_id (int): o\'chiriladigan kitobning ID raqami
    """
    deleted = service.delete_book(db, book_id)

    if not deleted:
        raise HTTPException(status_code=404, detail="Kitob topilmadi")

    return deleted