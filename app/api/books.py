import logging
from datetime import datetime
from typing import List

from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.db import repositories, schemas
from app.core.security import get_current_user
from app.core.config import get_db
from app.db.models import User

router = APIRouter()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@router.post("/", response_model=List[schemas.BookBase])
def create_book(book: schemas.BookBase, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    try:
        created_book = repositories.BookRepository.create_book(db=db, book=book)
        return [created_book]
    except IntegrityError as e:
        logger.error(f"Error creating book: {e}")
        raise HTTPException(status_code=400, detail="ISBN must be unique, there is only 1 kind unique book in this library")


@router.get("/", response_model=List[schemas.BookBase])
def read_books(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return repositories.BookRepository.get_all_books(db=db)


@router.get("/{isbn}", response_model=schemas.BookBase)
def read_book_by_isbn(isbn: str, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    db_book = repositories.BookRepository.get_book_by_isbn(db=db, isbn=isbn)
    if db_book is None:
        logger.error(f"Book with ISBN {isbn} not found")
        raise HTTPException(status_code=404, detail="Book not found")
    return db_book


@router.put("/{isbn}", response_model=schemas.BookBase)
def update_book(isbn: str, book: schemas.BookBase, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    db_book = repositories.BookRepository.get_book_by_isbn(db=db, isbn=isbn)
    if db_book is None:
        logger.error(f"Book with ISBN {isbn} not found")
        raise HTTPException(status_code=404, detail="Book not found")
    return repositories.BookRepository.update_book(db=db, isbn=isbn, book=book)


@router.delete("/{isbn}")
def delete_book(isbn: str, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    db_book = repositories.BookRepository.get_book_by_isbn(db=db, isbn=isbn)
    if db_book is None:
        logger.error(f"Book with ISBN {isbn} not found")
        raise HTTPException(status_code=404, detail="Book not found")
    repositories.BookRepository.delete_book(db=db, isbn=isbn)
    return {"message": "Book deleted successfully"}


@router.post("/checkout/{patron_id}/{isbn}")
def checkout_book(patron_id: int, isbn: str, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    patron = repositories.PatronRepository.get_patron_by_id(db=db, patron_id=patron_id)
    if patron is None:
        logger.error(f"Patron with ID {patron_id} not found")
        raise HTTPException(status_code=404, detail="Patron not found")

    book = repositories.BookRepository.get_book_by_isbn(db=db, isbn=isbn)
    if book is None:
        logger.error(f"Book with ISBN {isbn} not found")
        raise HTTPException(status_code=404, detail="Book not found")

    if book.checkout_date:
        logger.error(f"Book with ISBN {isbn} is already checked out")
        raise HTTPException(status_code=400, detail="Book is already checked out")

    book.checkout_date = datetime.now()
    book.checked_out_by_id = patron_id  # Associate the book with the patron who checked it out
    repositories.BookRepository.update_book(db=db, isbn=isbn,
                                            checkout_date=book.checkout_date,
                                            checked_out_by_id=book.checked_out_by_id)
    return {"message": "Book checked out successfully"}


@router.post("/return/{patron_id}/{isbn}")
def return_book(patron_id: int, isbn: str, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    patron = repositories.PatronRepository.get_patron_by_id(db=db, patron_id=patron_id)
    if patron is None:
        logger.error(f"Patron with ID {patron_id} not found")
        raise HTTPException(status_code=404, detail="Patron not found")

    book = repositories.BookRepository.get_book_by_isbn(db=db, isbn=isbn)
    if book is None:
        logger.error(f"Book with ISBN {isbn} not found")
        raise HTTPException(status_code=404, detail="Book not found")

    if not book.checkout_date:
        logger.error(f"Book with ISBN {isbn} is not checked out")
        raise HTTPException(status_code=400, detail="Book is not checked out")

    if book.checked_out_by_id != patron_id:
        logger.error(f"Book with ISBN {isbn} is not checked out by the current patron")
        raise HTTPException(status_code=400, detail="This book is not checked out by the current patron")

    # Update book status and associated patron
    book.checkout_date = None
    book.checked_out_by_id = None
    repositories.BookRepository.update_book(db=db, isbn=isbn,  checkout_date=book.checkout_date,
                                            checked_out_by_id=book.checked_out_by_id)
    return {"message": "Book returned successfully"}


@router.get("/checked-out-books/", response_model=List[schemas.BookBase])
def get_checked_out_books(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    checked_out_books = repositories.BookRepository.get_checked_out_books(db=db)
    return checked_out_books


@router.get("/overdue-books/", response_model=List[schemas.BookBase])
def get_overdue_books(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    overdue_books = repositories.BookRepository.get_overdue_books(db=db)
    return overdue_books
