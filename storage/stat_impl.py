from typing import Iterable
from storage.stat import Stat
from storage.stat import StatDAO
from pymongo.collection import Collection
from pymongo.database import Database
from pymongo import ASCENDING


class MongoStatDAO(StatDAO):

    def __init__(self, mongo_database: Database):
        self.database = mongo_database
        self.collection.create_index(
            [("ip", ASCENDING), ("resource", ASCENDING), ("timestamp", ASCENDING)]
        )

    @property
    def collection(self) -> Collection:
        return self.database['stat']

    @classmethod
    def to_bson(cls, stat: Stat):
        result = {
            k: v
            for k, v in stat.__dict__.items() if v is not None
        }
        return result

    def create(self, stat: Stat) -> Stat:
        return self.collection.insert_one(self.to_bson(stat))

    def stat_by_resource(self, resource: str, start: str, end: str) -> Iterable[dict]:
        pass

    def stat_by_ip(self, ip: str, start: str, end: str) -> Iterable[dict]:
        pass

    def stat_by_period(self, start: str, end: str) -> Iterable[Stat]:
        pass
