from datetime import datetime, timedelta
from typing import List, Optional

from sqlalchemy.orm import Session

from app.db import models
from app.db.schemas import BookBase, PatronBase


class BookRepository:
    @staticmethod
    def create_book(db: Session, book: BookBase) -> models.Book:
        db_book = models.Book(**book.dict())
        db.add(db_book)
        db.commit()
        db.refresh(db_book)
        return db_book

    @staticmethod
    def get_all_books(db: Session) -> List[models.Book]:
        return db.query(models.Book).all()

    @staticmethod
    def get_book_by_isbn(db: Session, isbn: str) -> Optional[models.Book]:
        return db.query(models.Book).filter(models.Book.isbn == isbn).first()

    @staticmethod
    def update_book(db: Session, isbn: str, **kwargs) -> Optional[models.Book]:
        db_book = db.query(models.Book).filter(models.Book.isbn == isbn).first()
        if db_book:
            for key, value in kwargs.items():
                setattr(db_book, key, value)
            db.commit()
            db.refresh(db_book)
            return db_book
        return None

    @staticmethod
    def delete_book(db: Session, isbn: str) -> bool:
        db_book = db.query(models.Book).filter(models.Book.isbn == isbn).first()
        if db_book:
            db.delete(db_book)
            db.commit()
            return True
        return False

    @staticmethod
    def get_checked_out_books(db: Session) -> List[models.Book]:
        return db.query(models.Book).filter(models.Book.checkout_date.isnot(None)).all()

    @staticmethod
    def get_overdue_books(db: Session) -> List[models.Book]:
        current_date = datetime.utcnow()
        overdue_books = db.query(models.Book).filter(models.Book.checkout_date < current_date - timedelta(days=7)).all()
        return overdue_books


class PatronRepository:
    @staticmethod
    def create_patron(db: Session, patron: PatronBase) -> models.Patron:
        db_patron = models.Patron(**patron.dict())
        db.add(db_patron)
        db.commit()
        db.refresh(db_patron)
        return db_patron

    @staticmethod
    def get_all_patrons(db: Session) -> List[models.Patron]:
        return db.query(models.Patron).all()

    @staticmethod
    def get_patron_by_id(db: Session, patron_id: int) -> Optional[models.Patron]:
        return db.query(models.Patron).filter(models.Patron.id == patron_id).first()

    @staticmethod
    def update_patron(db: Session, patron_id: int, patron: PatronBase) -> Optional[models.Patron]:
        db_patron = db.query(models.Patron).filter(models.Patron.id == patron_id).first()
        if db_patron:
            for key, value in patron.dict().items():
                setattr(db_patron, key, value)
            db.commit()
            db.refresh(db_patron)
            return db_patron
        return None

    @staticmethod
    def delete_patron(db: Session, patron_id: int) -> bool:
        db_patron = db.query(models.Patron).filter(models.Patron.id == patron_id).first()
        if db_patron:
            db.delete(db_patron)
            db.commit()
            return True
        return False


class UserRepository:
    @staticmethod
    def authenticate_user(db: Session, username: str, password: str) -> models.User:
        return db.query(models.User).filter(models.User.username == username, models.User.password == password).first()

    @staticmethod
    def get_user_by_id(db: Session, user_id: int) -> models.User:
        return db.query(models.User).filter(models.User.id == user_id).first()

    @staticmethod
    def create_user(db: Session, username: str, password: str) -> models.User:
        user = models.User(username=username, password=password)
        db.add(user)
        db.commit()
        db.refresh(user)
        return user

    @staticmethod
    def update_user(db: Session, user_id: int, username: str, password: str) -> models.User:
        user = db.query(models.User).filter(models.User.id == user_id).first()
        if user:
            user.username = username
            user.password = password
            db.commit()
            db.refresh(user)
            return user
        return None

    @staticmethod
    def delete_user(db: Session, user_id: int) -> bool:
        user = db.query(models.User).filter(models.User.id == user_id).first()
        if user:
            db.delete(user)
            db.commit()
            return True
        return False
