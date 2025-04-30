import motor.motor_asyncio
import os
from motor.motor_asyncio import AsyncIOMotorClient

MONGODB_URL = os.getenv("MONGODB_URL", "mongodb://mongo_admin:password@localhost:27017")

client = motor.motor_asyncio.AsyncIOMotorClient(MONGODB_URL)

db = client.library_db

books_collection = db.books