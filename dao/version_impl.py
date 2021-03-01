from pymongo.collection import Collection
from pymongo.database import Database
from dao.interfaces.version import LibraryVersion, LibraryVersionDAO


class MongoVersionDAO(LibraryVersionDAO):

    def __init__(self, mongo_database: Database):
        self.database = mongo_database

    def create(self, version: LibraryVersion):
        version = self.collection.insert_one(self.to_bson(version))
        return version

    @property
    def collection(self) -> Collection:
        return self.database['lversion']

    @classmethod
    def to_bson(cls, version: LibraryVersion):
        result = {
            k: v
            for k, v in version.__dict__.items() if v is not None
        }
        return result

    @classmethod
    def from_bson(cls, document) -> LibraryVersion:
        document['id'] = str(document.pop('_id'))
        return LibraryVersion(**document)

    def get_version(self):
        return self.from_bson(self.collection.find_one())
