from fastapi import FastAPI, HTTPException
from typing import List
from app.models import fake_books_db
from app.schemas import BookSchema
from marshmallow import ValidationError
from fastapi.responses import JSONResponse

app = FastAPI()

book_schema = BookSchema()
books_schema = BookSchema(many=True)

@app.get("/books", response_model=List[dict])
async def get_books():
    return fake_books_db

@app.get("/books/{book_id}", response_model=dict)
async def get_book(book_id: int):
    for book in fake_books_db:
        if book["id"] == book_id:
            return book
    raise HTTPException(status_code=404, detail="Book not found")

@app.post("/books", response_model=dict)
async def create_book(book: dict):
    try:
        valid_book = book_schema.load(book)
    except ValidationError as err:
        raise HTTPException(status_code=400, detail=err.messages)

    new_book = valid_book
    new_book["id"] = len(fake_books_db) + 1 
    fake_books_db.append(new_book)
    return new_book

@app.delete("/books/{book_id}", response_model=dict)
async def delete_book(book_id: int):
    for book in fake_books_db:
        if book["id"] == book_id:
            fake_books_db.remove(book)
            return book
    raise HTTPException(status_code=404, detail="Book not found")
