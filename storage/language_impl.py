from typing import Iterable
import bson
import bson.errors
from pymongo.collection import Collection
from pymongo.database import Database
from pymongo import ASCENDING
from storage.language import Language, LanguageDAO, LanguageNotFound


class MongoLanguageDAO(LanguageDAO):

    def __init__(self, mongo_database: Database):
        self.database = mongo_database

    @property
    def collection(self) -> Collection:
        return self.database['language']

    @classmethod
    def to_bson(cls, language: Language):
        result = {
            k: v
            for k, v in language.__dict__.items() if v is not None
        }
        if 'id' in result:
            result['_id'] = result.pop('id')
        return result

    @classmethod
    def from_bson(cls, document) -> Language:
        document['id'] = str(document.pop('_id'))
        return Language(**document)

    def create(self, language: Language) -> Language:
        one_language = self.collection.insert_one(self.to_bson(language))
        #  one_language.id = str(one_language.inserted_id)
        return one_language

    def update(self, language: Language) -> Language:
        pass

    def get_all(self) -> Iterable[Language]:
        for document in self.collection.find():
            yield self.from_bson(document)

    def get_by_id(self, language_id: str) -> Language:
        document = self.collection.find_one({'_id': language_id})
        if document is None:
            raise LanguageNotFound
        return self.from_bson(document)

