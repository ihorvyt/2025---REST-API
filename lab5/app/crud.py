from app.database import books_collection
from app.models import BookCreate, BookUpdate, Book, BookInDB
from pydantic_mongo import PydanticObjectId
from typing import List, Optional
from bson import ObjectId

async def create_book(book: BookCreate) -> BookInDB:
    book_dict = book.dict()
    
    result = await books_collection.insert_one(book_dict)
    book_dict["_id"] = result.inserted_id
    
    return BookInDB(**book_dict)




async def get_all_books(limit: int = 10, cursor: Optional[str] = None) -> List[BookInDB]:
    query = {}
    if cursor:
        try:
            query["_id"] = {"$gt": ObjectId(cursor)}
        except:
            raise ValueError("Invalid cursor format")
    
    books = []
    cursor_obj = books_collection.find(query).sort("_id", 1).limit(limit)
    
    async for document in cursor_obj:
        books.append(BookInDB(**document))
    
    return books



async def get_book(book_id: PydanticObjectId) -> Optional[BookInDB]:
    book = await books_collection.find_one({"_id": book_id})
    
    if book:
        return BookInDB(**book)
    
    return None


async def update_book(book_id: PydanticObjectId, book_update: BookUpdate) -> Optional[BookInDB]:
    update_data = {k: v for k, v in book_update.dict().items() if v is not None}
    
    if update_data:
        await books_collection.update_one(
            {"_id": book_id},
            {"$set": update_data}
        )
    
    return await get_book(book_id)


async def delete_book(book_id: PydanticObjectId) -> bool:
    result = await books_collection.delete_one({"_id": book_id})
    
    return result.deleted_count > 0