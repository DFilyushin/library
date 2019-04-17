from typing import Iterable
import bson
import bson.errors
from pymongo.collection import Collection
from pymongo.database import Database
from pymongo import ASCENDING
from pymongo.errors import DuplicateKeyError
from storage.genre import Genre, GenreDAO, GenreNotFound, NewGenre, NewGenreDAO


class MongoGenreDAO(GenreDAO):

    def __init__(self, mongo_database: Database):
        self.database = mongo_database
        self.collection.create_index(
            [("slug", ASCENDING)],
            unique=True
        )

    @property
    def collection(self) -> Collection:
        return self.database['genres']

    @classmethod
    def to_bson(cls, genre: Genre):
        result = {
            k: v
            for k, v in genre.__dict__.items() if v is not None
        }
        if 'id' in result:
            result['_id'] = bson.ObjectId(result.pop('id'))
        return result

    @classmethod
    def to_bson_many(cls, genres):
        result = []
        for x in genres:
            item = {
                k: v
                for k, v in x.__dict__.items() if v is not None
            }
            if 'id' in result:
                result['_id'] = bson.ObjectId(result.pop('id'))
            result.append(item)
        return result

    @classmethod
    def from_bson(cls, document) -> Genre:
        document['id'] = str(document.pop('_id'))
        return Genre(**document)

    def create(self, genre: Genre) -> Genre:
        one_genre = self.collection.insert_one(self.to_bson(genre))
        genre.id = str(one_genre.inserted_id)
        return genre

    def update(self, genre: Genre) -> Genre:
        genre_id = bson.ObjectId(genre.id)
        self.collection.update_one(
            {'_id': genre_id},
            {'$set': self.to_bson(genre)}
        )
        return genre

    def _get_by_query(self, query) -> Genre:
        document = self.collection.find_one(query).collation({'locale': 'en', 'strength': 2})
        if document is None:
            raise GenreNotFound
        return self.from_bson(document)

    def get_all(self) -> Iterable[Genre]:
        for document in self.collection.find():
            yield self.from_bson(document)

    def get_by_id(self, genre_id: str) -> Genre:
        return self._get_by_query({'id': genre_id})

    def get_by_slug(self, slug: str) -> Genre:
        return self._get_by_query({'slug': slug})


class MongoNewGenreDAO(NewGenreDAO):

    def __init__(self, mongo_database: Database):
        self.database = mongo_database

    @property
    def collection(self) -> Collection:
        return self.database['genres_main']

    @classmethod
    def to_bson(cls, genre: NewGenre):
        result = {
            k: v
            for k, v in genre.__dict__.items() if v is not None
        }
        if 'id' in result:
            result['_id'] = result.pop('id')
        return result

    @classmethod
    def to_bson_many(cls, genres):
        result = []
        for x in genres:
            item = {
                k: v
                for k, v in x.__dict__.items() if v is not None
            }
            if 'id' in result:
                result['_id'] = result.pop('id')
            result.append(item)
        return result

    @classmethod
    def from_bson(cls, document) -> NewGenre:
        document['id'] = str(document.pop('_id'))
        return NewGenre(**document)

    def create(self, genre: NewGenre) -> NewGenre:
        one_genre = self.collection.insert_one(self.to_bson(genre))
        genre.id = str(one_genre.inserted_id)
        return genre

    def update(self, genre: NewGenre) -> NewGenre:
        genre_id = bson.ObjectId(genre.id)
        self.collection.update_one(
            {'_id': genre_id},
            {'$set': self.to_bson(genre)}
        )
        return genre

    def get_all(self) -> Iterable[Genre]:
        for document in self.collection.find({'parent': ''}):
            sub_genres = []
            for sub_document in self.collection.find({'parent': document['_id']}):
                sub_genres.append(self.from_bson(sub_document))
            document['sub_genres'] = sub_genres
            yield self.from_bson(document)

    def get_by_id(self, genre_id: str) -> NewGenre:
        pass
