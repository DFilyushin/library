from typing import Iterable
import bson
import bson.errors
from pymongo.collection import Collection
from pymongo.database import Database
from pymongo import ASCENDING
from dao.interfaces.genre import Genre, GenreDAO, GenreNotFound


class MongoGenreDAO(GenreDAO):

    def __init__(self, mongo_database: Database):
        self.database = mongo_database
        self.collection.create_index(
            [("parent", ASCENDING)],
            unique=False
        )

    @property
    def collection(self) -> Collection:
        return self.database['genres_main']

    @classmethod
    def to_bson(cls, genre: Genre):
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

    def get_all(self) -> Iterable[Genre]:
        for document in self.collection.find({'parent': ''}):
            counter = 0
            sub_genres = []
            sql = [
                {"$project": {"_id": 0, "genres_main": "$$ROOT"}},
                {"$match": {'genres_main.parent': document['_id']}},
            ]
            for sub_document in self.collection.aggregate(sql):
                sub_genres.append(sub_document)
            document['sub_genres'] = [row['genres_main'] for row in sub_genres]
            yield self.from_bson(document)

    def get_by_id(self, genre_id: str) -> Genre:
        pass
