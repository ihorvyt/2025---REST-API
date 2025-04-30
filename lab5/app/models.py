from pydantic import BaseModel, Field
from pydantic_mongo import ObjectIdField, PydanticObjectId
from typing import Optional, List


class BookBase(BaseModel):
    title: str
    author: str
    year: int
    genre: Optional[str] = None
    pages: Optional[int] = None


class BookCreate(BookBase):
    pass


class BookUpdate(BaseModel):
    title: Optional[str] = None
    author: Optional[str] = None
    year: Optional[int] = None
    genre: Optional[str] = None
    pages: Optional[int] = None


class BookInDB(BookBase):
    id: PydanticObjectId = Field(default_factory=PydanticObjectId, alias="_id")

    class Config:
        orm_mode = True
        allow_population_by_field_name = True
        json_encoders = {
            PydanticObjectId: str
        }


class Book(BookInDB):
    pass