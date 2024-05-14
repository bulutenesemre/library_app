from fastapi import FastAPI

from app.api import books, patrons
from app.core.config import create_database

app = FastAPI()

create_database()

app.include_router(books.router, prefix="/books", tags=["books"])
app.include_router(patrons.router, prefix="/patrons", tags=["patrons"])
