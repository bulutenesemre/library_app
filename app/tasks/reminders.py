from celery import shared_task

from app.db import repositories
from app.utils.email import send_email
from app.core.config import get_db


@shared_task
def send_email_reminder():
    db = get_db()
    overdue_books = repositories.BookRepository.get_overdue_books(db)
    for book in overdue_books:
        patron = repositories.PatronRepository.get_patron_by_id(db, book.checked_out_by_id)
        if patron and patron.email:
            send_email(patron.email, book.title)
