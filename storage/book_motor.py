from typing import Iterable
import asyncio
import bson
import bson.errors
from motor.motor_asyncio import AsyncIOMotorDatabase as Database
from motor.motor_asyncio import AsyncIOMotorCollection as Collection
from pymongo.database import Database
from storage.book import Book, BookDAO, BookNotFound


class MotorBookDAO(BookDAO):

    def __init__(self, mongo_database: Database):
        self.database = mongo_database
        self.loop = asyncio.get_event_loop()
        self._collection = self.database['books']

    @property
    async def collection(self) -> Collection:
        # return self.database['books']
        await 0

    @classmethod
    def to_bson(cls, book: Book):
        result = {
            k: v
            for k, v in book.__dict__.items() if v is not None
        }
        if 'id' in result:
            result['_id'] = bson.ObjectId(result.pop('id'))
        return result

    @classmethod
    def to_bson_many(cls, books):
        result = []
        for x in books:
            item = {
                k: v
                for k, v in x.__dict__.items() if v is not None
            }
            if 'id' in result:
                result['_id'] = bson.ObjectId(result.pop('id'))
            result.append(item)
        return result

    @classmethod
    async def from_bson(cls, document) -> Book:
        document['id'] = str(document.pop('_id'))
        return Book(**document)

    async def _create(self, book: Book) -> Book:
        self._collection.insert_one(self.to_bson(book))
        # one_book = await self._collection.insert_one(self.to_bson(book))
        # book.id = str(one_book.inserted_id)
        # await book
        # return self.loop.run_until_complete(asyncio.gather(*futures))

    def create(self, book: Book) -> Book:
        self.loop.run_until_complete(self._create(book))

    async def _create_many(self, books: list):
        self._collection.insert_many(self.to_bson_many(books))

    def create_many(self, books: list):
        self.loop.run_until_complete(self._create_many(books))

    async def update(self, book: Book) -> Book:
        book_id = bson.ObjectId(book.id)
        self.collection.update_one(
            {'_id': book_id},
            {'$set': self.to_bson(book)}
        )
        return book

    async def get_all(self) -> Iterable[Book]:
        async for document in self.collection.find():
            await self.to_bson(document)

    async def _get_by_query(self, query) -> Book:
        document = self.collection.find_one(query)
        if document is None:
            raise BookNotFound
        return self.from_bson(document)

    async def get_by_slug(self, slug: str)->Book:
        return self._get_by_query({'slug': slug})

    async def get_by_id(self, book_id: str):
        return self._get_by_query({'_id': bson.ObjectId(book_id)})
        self.authors = authors


    async def get_by_author(self, author: str) -> Book:
        pass

    async def get_by_name(self, name: str) -> Book:
        pass
