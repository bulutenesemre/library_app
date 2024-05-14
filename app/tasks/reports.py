from celery import shared_task
from datetime import timedelta

from app.core.config import get_db
from app.db.repositories import BookRepository


@shared_task
def generate_weekly_report():
    db = get_db()
    checked_out_books = BookRepository.get_checked_out_books(db)

    # Generate report
    report = []
    for book in checked_out_books:
        report.append({
            'title': book.title,
            'patron_name': book.patron.name,
            'checkout_date': book.checkout_date,
            'due_date': book.checkout_date + timedelta(days=7),
        })

    for entry in report:
        print(entry)
