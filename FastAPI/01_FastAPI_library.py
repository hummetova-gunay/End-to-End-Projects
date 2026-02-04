# Task 1: Book Library

# Create a simple book library API with 
# - a dictionary storing books (id as key, book details as value: title, author, year)
# - GET endpoint to retrieve all books
# - GET endpoint to retrieve a book by ID
# - POST endpoint to add a new book
# - DELETE endpoint to remove a book

from fastapi import FastAPI, Path
from typing import Optional
from pydantic import BaseModel

app = FastAPI()

# - a dictionary storing books (id as key, book details as value: title, author, year)
books = {
    1:{
        'title': 'title1',
        'author': 'Author1',
        'year': 2001
    },
    2:{
        'title': 'title2',
        'author': 'Author2',
        'year': 2002
    },
    3:{
        'title': 'title3',
        'author': 'Author3',
        'year': 2003
    },
    4:{
        'title': 'title4',
        'author': 'Author4',
        'year': 2004
    }
}

# - GET endpoint to retrieve all books

@app.get('/get-all-books')
def get_all_books():
    return books


# - GET endpoint to retrieve a book by ID
@app.get('/get-book/{book_id}')
def get_book(book_id: int):
    return books[book_id]

# - POST endpoint to add a new book
class Book(BaseModel):
    title: str
    author: str
    year: int


@app.post('/create-book/{book_id}')
def create_book(book_id: int, book: Book):
    if book_id in books:
        return {'Error': 'This book already exists'}
    books[book_id]= book
    return books

# - DELETE endpoint to remove a book

@app.delete('/delete-books/{book_id}')
def delete_book(book_id: int):
    if book_id not in books:
        return {'Error':'This book does not exist'}
    del books[book_id]
    return books