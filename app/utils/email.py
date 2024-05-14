import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from dotenv import load_dotenv
import os

load_dotenv()


def send_email(recipient_email, book_title):
    load_dotenv()

    sender_email = os.getenv("sender_email")
    sender_password = os.getenv("sender_password")
    smtp_server = os.getenv("smtp_server")
    smtp_port = os.getenv("smtp_port")

    # Create message
    message = MIMEMultipart()
    message['From'] = sender_email
    message['To'] = recipient_email
    message['Subject'] = "Reminder: Return Overdue Book"
    body = (f"Dear Patron,\n\nThis is a reminder that the book '{book_title}' is overdue. Please return it to the "
            f"library at your earliest convenience.\n\nSincerely,\nThe Library")
    message.attach(MIMEText(body, 'plain'))

    try:
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            server.send_message(message)
        print(f"Reminder email sent to {recipient_email} for book '{book_title}'")
    except smtplib.SMTPException as e:
        print(f"Failed to send reminder email to {recipient_email}: {e}")
