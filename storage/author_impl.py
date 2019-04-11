from typing import Iterable
import bson
import bson.errors
from pymongo.collection import Collection
from pymongo.database import Database
from pymongo import ASCENDING
from pymongo.errors import DuplicateKeyError
from storage.author import Author, AuthorDAO, AuthorNotFound


class MongoAuthorDAO(AuthorDAO):

    def __init__(self, mongo_database: Database):
        self.database = mongo_database
        self.collection.create_index(
            [("last_name", ASCENDING), ("first_name", ASCENDING), ("middle_name", ASCENDING)],
            unique=True
        )

    @property
    def collection(self) -> Collection:
        return self.database['authors']

    @classmethod
    def to_bson(cls, author: Author):
        result = {
            k: v
            for k, v in author.__dict__.items() if v is not None
        }
        if 'id' in result:
            result['_id'] = bson.ObjectId(result.pop('id'))
        return result

    @classmethod
    def to_bson_many(cls, authors):
        result = []
        for x in authors:
            item = {
                k: v
                for k, v in x.__dict__.items() if v is not None
            }
            if 'id' in result:
                result['_id'] = bson.ObjectId(result.pop('id'))
            result.append(item)
        return result

    @classmethod
    def from_bson(cls, document) -> Author:
        document['id'] = str(document.pop('_id'))
        return Author(**document)

    def create(self, author: Author) -> Author:
        one_author = self.collection.insert_one(self.to_bson(author))
        author.id = str(one_author.inserted_id)
        return author

    def update(self, author: Author) -> Author:
        book_id = bson.ObjectId(author.id)
        self.collection.update_one(
            {'_id': book_id},
            {'$set': self.to_bson(author)}
        )
        return author

    def get_all(self) -> Iterable[Author]:
        for document in self.collection.find():
            yield self.from_bson(document)

    def _get_by_query(self, query) -> Iterable[Author]:
        documents = self.collection.find(query).collation({'locale': 'en', 'strength': 2})
        if documents is None:
            raise AuthorNotFound
        for document in documents:
            yield self.from_bson(document)

    def get_by_id(self, author_id: str):
        document = self.collection.find_one({'_id': bson.ObjectId(author_id)})
        if document is None:
            raise AuthorNotFound('Not found author by id {}'.format(author_id))
        return self.from_bson(document)

    def get_by_last_name(self, last_name: str) -> Iterable[Author]:
        return self._get_by_query({'last_name': last_name})

    def get_by_names(self, first_name: str, last_name: str, middle_name: str) -> Author:
        document = self.collection.\
            find_one({'last_name': last_name, 'first_name': first_name, 'middle_name': middle_name})
            #collation({'locale': 'en', 'strength': 2})
        if document is None:
            raise AuthorNotFound
        return self.from_bson(document)

    def get_by_start(self, start_text: str, limit: int, skipped: int):
        documents = self.collection.\
            find({'last_name': {'$regex': '^' + start_text, '$options': 'i'}}).\
            collation({'locale': 'en', 'strength': 2}).skip(skipped)
        if limit > 0:
            documents = documents.limit(limit)
        if documents is None:
            raise AuthorNotFound
        for document in documents:
            yield self.from_bson(document)
