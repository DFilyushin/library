from typing import Iterable
import bson
import bson.errors
import pymongo
from pymongo.collection import Collection
from pymongo.database import Database

from storage.book import Book, BookDAO, BookNotFound


class MongoBookDAO(BookDAO):

    def __init__(self, mongo_database: Database):
        self.database = mongo_database


    @property
    def collection(self) -> Collection:
        return self.database['books']

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
    def from_bson(cls, document) -> Book:
        document['id'] = str(document.pop('_id'))
        return Book(**document)

    def create(self, book: Book) -> Book:
        one_book = self.collection.insert_one(self.to_bson(book))
        book.id = str(one_book.inserted_id)
        return book

    def create_many(self, books: list):
        self.collection.insert_many(self.to_bson_many(books))

    def update(self, book: Book) -> Book:
        book_id = bson.ObjectId(book.id)
        self.collection.update_one(
            {'_id': book_id},
            {'$set': self.to_bson(book)}
        )
        return book

    def get_all(self) -> Iterable[Book]:
        for document in self.collection.find():
            yield self.from_bson(document)

    def _get_one_by_query(self, query) -> Book:
        document = self.collection.find_one(query)
        if document is None:
            raise BookNotFound
        return self.from_bson(document)

    def _get_many_by_query(self, query) -> Iterable[Book]:
        documents = self.collection.find(query)
        if documents is None:
            raise BookNotFound
        for document in documents:
            yield self.from_bson(document)

    def get_by_slug(self, slug: str)->Book:
        return self._get_one_by_query({'slug': slug})

    def get_by_id(self, book_id: str):
        return self._get_one_by_query({'_id': bson.ObjectId(book_id)})

    def get_by_author(self, author: str) -> Book:
        return self._get_many_by_query('{}')

    def get_by_name(self, name: str) -> Book:
        return self._get_many_by_query('{}')
