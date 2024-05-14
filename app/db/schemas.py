from pydantic import BaseModel


class BookBase(BaseModel):
    title: str
    author: str
    isbn: str


class PatronBase(BaseModel):
    name: str
    email: str


class UserBase(BaseModel):
    username: str
    password: str
