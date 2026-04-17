from sqlalchemy.orm import Session
from app.models.book import Book


class BookService:
    """
    Kitoblar bilan ishlash uchun servis klassi.

    Ushbu klass ma'lumotlar bazasida kitoblarni yaratish,
    o\'qish, yangilash va o\'chirish (CRUD) amallarini bajaradi.
    """

    def get_all_books(self, db: Session):
        """
        Ma'lumotlar bazasidagi barcha kitoblarni olish.

        Parametrlar:
        db (Session): SQLAlchemy database sessiyasi.

        Natija:
        list: barcha kitoblar ro\'yxati.
        """
        return db.query(Book).all()

    def get_book_by_id(self, db: Session, book_id: int):
        """
        Berilgan ID bo\'yicha kitobni olish.

        Parametrlar:
        db (Session): database sessiyasi
        book_id (int): kitobning ID raqami

        Natija:
        Book | None: topilgan kitob yoki None
        """
        return db.query(Book).filter(Book.id == book_id).first()

    def create_book(self, db: Session, book):
        """
        Yangi kitob yaratish va ma'lumotlar bazasiga saqlash.

        Parametrlar:
        db (Session): database sessiyasi
        book: foydalanuvchi yuborgan kitob ma'lumotlari

        Natija:
        Book: yaratilgan kitob
        """
        new_book = Book(**book.dict())

        db.add(new_book)
        db.commit()
        db.refresh(new_book)

        return new_book

    def update_book(self, db: Session, book_id: int, book):
        """
        Mavjud kitob ma'lumotlarini yangilash.

        Parametrlar:
        db (Session): database sessiyasi
        book_id (int): yangilanadigan kitob ID si
        book: yangi kitob ma'lumotlari

        Natija:
        Book | None: yangilangan kitob yoki None
        """
        db_book = db.query(Book).filter(Book.id == book_id).first()

        if not db_book:
            return None

        for key, value in book.dict().items():
            setattr(db_book, key, value)

        db.commit()
        db.refresh(db_book)

        return db_book

    def delete_book(self, db: Session, book_id: int):
        """
        Berilgan ID bo\'yicha kitobni o\'chirish.

        Parametrlar:
        db (Session): database sessiyasi
        book_id (int): o\'chiriladigan kitob ID si

        Natija:
        dict | None: o\'chirilganligi haqida xabar yoki None
        """
        db_book = db.query(Book).filter(Book.id == book_id).first()

        if not db_book:
            return None

        db.delete(db_book)
        db.commit()

        return {"message": "Book deleted"}