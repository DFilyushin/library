from typing import Iterable
import bson
import bson.errors
from pymongo import ASCENDING
from pymongo.collection import Collection
from pymongo.database import Database
from storage.book import Book, BookDAO, BookNotFound


class MongoBookDAO(BookDAO):

    def __init__(self, mongo_database: Database):
        self.database = mongo_database
        self.collection.create_index(
            [("authors", ASCENDING)],
            unique=False
        )
        self.collection.create_index(
            [('genres', ASCENDING)],
            unique=False
        )
        self.collection.create_index(
            [('keywords', ASCENDING)],
            unique=False
        )
        self.collection.create_index(
            [('name', ASCENDING)],
            unique=False
        )
        self.collection.create_index(
            [('filename', ASCENDING)],
            unique=False
        )

    @property
    def collection(self) -> Collection:
        return self.database['books']

    @classmethod
    def to_bson(cls, book: Book):
        result = {
            k: v
            for k, v in book.__dict__.items() if v is not None
        }
        # if 'id' in result:
            # result['_id'] = result.get('filename')
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
        document['id'] = str(document.get('filename', ''))
        return Book(**document)

    def create(self, book: Book) -> Book:
        one_book = self.collection.insert_one(self.to_bson(book))
        book.id = str(one_book.inserted_id)
        return book

    def create_many(self, books: list):
        self.collection.insert_many(self.to_bson_many(books))

    def update(self, book: Book) -> Book:
        book_id =book.filename
        self.collection.update_one(
            {'filename': book_id},
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
        try:
            documents = self.collection.aggregate([
                {"$match": {'filename': book_id}},
                {"$lookup":
                    {
                        'from': 'authors',
                        'localField': 'authors',
                        'foreignField': '_id',
                        'as': 'authors'
                    }
                }
            ])
        except bson.errors.InvalidId:
            return None
        try:
            value = next(documents)
        except StopIteration:
            return None
        return self.from_bson(value)

    def get_by_author(self, author: str) -> Iterable[Book]:
        try:
            obj_author = bson.ObjectId(author)
        except bson.errors.InvalidId:
            return None
        yield from self.search_book(author=obj_author)

    def get_by_name(self, name: str) -> Book:
        yield from self.search_book(name=name)

    def search_book(self, name: str = None, author: str = None,  lang: str = None,
                    series: str = None, keyword: str = None, genre: str = None,
                    limit: int = 100, skip: int = 0):
        match = {'deleted': False}
        if name:
            match['name'] = {'$regex': name, '$options': 'i'}
        if lang:
            match['lang'] = lang
        if series:
            match['series'] = series
        if keyword:
            match['keywords'] = keyword
        if author:
            match['authors'] = author
        if genre:
            match['genres'] = genre
        documents = self.collection.aggregate([
            {"$match": match},
            {"$skip": int(skip)},
            {"$limit": int(limit)},
            {"$lookup":
                {
                    'from': 'authors',
                    'localField': 'authors',
                    'foreignField': '_id',
                    'as': 'authors',
                }
            },
            {"$lookup":
                {
                    'from': 'genres_main',
                    'localField': 'genres',
                    'foreignField': '_id',
                    'as': 'genres',
                }
            },
        ])
        for document in documents:
            yield self.from_bson(document)

    def books_by_genres(self, genre: str):
        yield from self.search_book(genre=genre)

    def get_count_books(self):
        result = self.collection.find({'deleted': False}).count()
        return result

    def get_genres_by_author(self, id: str):
        obj_author = bson.ObjectId(id)
        documents = self.collection.aggregate([
            {"$unwind": {"path": "$genres"}},
            {"$match": {'authors': obj_author}},
            {"$project": {"genres": "$genres", "_id": 0}},
            {"$group": {"_id": None, "distinct": {"$addToSet": "$$ROOT"}}},
            {"$unwind": {"path": "$distinct", "preserveNullAndEmptyArrays" : False}},
            {"$replaceRoot": {"newRoot" : "$distinct"}}
        ])
        for document in documents:
            yield document

    def books_by_language(self, languageId, limit: int, skip: int):
        yield from self.search_book(lang=languageId, limit=limit, skip=skip)

    def get_languages_by_books(self):
        documents = self.collection.aggregate([
            {"$unwind": {"path": "$genres"}},
            {"$project": {"lang": "$lang", "_id": 0}},
            {"$group": {"_id": None, "distinct": {"$addToSet": "$$ROOT"}}},
            {"$unwind": {"path": "$distinct", "preserveNullAndEmptyArrays" : False}},
            {"$replaceRoot": {"newRoot" : "$distinct"}}
        ])
        for document in documents:
            yield document

    def get_book_by_filename(self, filename: str):
        try:
            documents = self.collection.aggregate([
                {"$match": {'filename': filename}},
                {"$lookup":
                    {
                        'from': 'authors',
                        'localField': 'authors',
                        'foreignField': '_id',
                        'as': 'authors'
                    }
                }
            ])
        except bson.errors.InvalidId:
            return None
        try:
            value = next(documents)
        except StopIteration:
            return None
        return self.from_bson(value)

    def get_popular_books(self, limit: int):
        query = [
            {"$match": {"action": "bv"}},
            {"$group": {"_id": {"resource": "$resource"}, "COUNT(*)": {"$sum": 1}}},
            {"$project": {"resource": "$_id.resource", "cnt": "$COUNT(*)","_id": 0}},
            {"$sort": {"cnt": -1}},
            {"$limit": limit}
        ]
        documents = self.collection.aggregate(query)
        for document in documents:
            document['book_id'] = document['resource']
            yield document

