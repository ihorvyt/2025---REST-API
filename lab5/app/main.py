from fastapi import FastAPI, HTTPException, status, Depends
from app.models import Book, BookCreate, BookUpdate, BookInDB
from app.crud import create_book, get_book, get_all_books, update_book, delete_book
from pydantic_mongo import PydanticObjectId
from typing import List

app = FastAPI(title="Library API", description="API for managing library books", version="1.0.0")


@app.get("/")
async def root():
    return {"message": "Welcome to the Library API"}


@app.post("/books/", response_model=Book, status_code=status.HTTP_201_CREATED)
async def create_new_book(book: BookCreate):
    return await create_book(book)


@app.get("/books/", response_model=List[Book])
async def read_books():
    return await get_all_books()


@app.get("/books/{book_id}", response_model=Book)
async def read_book(book_id: str):
    try:
        book_oid = PydanticObjectId(book_id)
    except:
        raise HTTPException(status_code=400, detail="Invalid book ID format")
    
    book = await get_book(book_oid)
    if book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    
    return book


@app.put("/books/{book_id}", response_model=Book)
async def update_existing_book(book_id: str, book_update: BookUpdate):
    try:
        book_oid = PydanticObjectId(book_id)
    except:
        raise HTTPException(status_code=400, detail="Invalid book ID format")
    
    book = await update_book(book_oid, book_update)
    if book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    
    return book


@app.delete("/books/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_existing_book(book_id: str):
    try:
        book_oid = PydanticObjectId(book_id)
    except:
        raise HTTPException(status_code=400, detail="Invalid book ID format")
    
    deleted = await delete_book(book_oid)
    if not deleted:
        raise HTTPException(status_code=404, detail="Book not found")
    
    return None