from pymongo.collection import Collection
from pymongo.database import Database
from storage.version import LibraryVersion, LibraryVersionDAO, VersionNotFound


class MongoVersionDAO(LibraryVersionDAO):

    def __init__(self, mongo_database: Database):
        self.database = mongo_database

    def create(self, version: LibraryVersion):
        version = self.collection.insert_one(self.to_bson(version))
        return version

    @property
    def collection(self) -> Collection:
        value = self.database['lversion']
        return value

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
        item = self.collection.find_one()
        if not item:
            raise VersionNotFound
        return self.from_bson(item)
