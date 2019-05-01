from typing import Iterable
import bson
import bson.errors
from pymongo.collection import Collection
from pymongo.database import Database
from pymongo import ASCENDING
from pymongo.errors import DuplicateKeyError
from storage.starred_book import StarredBook, StarredBookDAO, StarExists


class MongoStarredBook(StarredBookDAO):
    def __init__(self, mongo_database: Database):
        self.database = mongo_database
        self.collection.create_index(
            [
                ("login", ASCENDING),
                ("book_id", ASCENDING)
            ],
            unique=True
        )

    @property
    def collection(self) -> Collection:
        return self.database['stars']

    @classmethod
    def to_bson(cls, user: StarredBook):
        result = {
            k: v
            for k, v in user.__dict__.items() if v is not None
        }
        if 'id' in result:
            result['_id'] = bson.ObjectId(result.pop('id'))
        return result

    @classmethod
    def from_bson(cls, document) -> StarredBook:
        document['id'] = str(document.pop('_id'))
        return StarredBook(**document)

    def create(self, star: StarredBook)->StarredBook:
        try:
            one_star = self.collection.insert_one(self.to_bson(star))
        except DuplicateKeyError:
            raise StarExists
        star.id = str(one_star.inserted_id)
        return star

    def get_by_id(self, star_id: str)->StarredBook:
        document = self.collection.find_one({'_id': bson.ObjectId(star_id)})
        return self.from_bson(document)

    def get_by_login(self, login: str)->Iterable[StarredBook]:
        documents = self.collection.find({'book_id': login})
        for document in documents:
            yield self.from_bson(document)

    def get_by_book(self, book_id: str)->Iterable[StarredBook]:
        documents = self.collection.find({'book_id': book_id})
        for document in documents:
            yield self.from_bson(document)

    def delete(self, id: str)->bool:
        return self.collection.delete_one({id: bson.ObjectId(id)})

    def delete_by_star_pair(self, login: str, book_id: str)->bool:
        return self.collection.delete_one({'login': login, 'book_id': book_id})

    def delete_by_login(self, login:str)->bool:
        return self.collection.delete_many({'login': login})

    def delete_by_book(self, book_id:str)->bool:
        return self.collection.delete_many({'book_id': book_id})
