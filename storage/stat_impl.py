import re
from typing import Iterable
from storage.stat import Stat
from storage.stat import StatDAO
from pymongo.collection import Collection
from pymongo.database import Database
from pymongo import ASCENDING
from datetime import datetime


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

    @classmethod
    def from_bson(cls, document) -> Stat:
        document['id'] = str(document.pop('_id'))
        return Stat(**document)

    def create(self, stat: Stat) -> Stat:
        return self.collection.insert_one(self.to_bson(stat))

    def stat_by_resource(self, resource: str, start: str, end: str) -> Iterable[dict]:
        pass

    def stat_by_ip(self, ip: str, start: str, end: str) -> Iterable[dict]:
        pass

    def stat_by_period(self, start: str, end: str) -> Iterable[Stat]:
        pass

    def downloads_by_login(self, login: str)->int:
        query = [
            {"$match": {
                "action": "bd",
                "login": login
            }
            },
            {"$group": {"_id": {}, "COUNT(*)": {"$sum": 1}}},
            {"$project": {"cnt": "$COUNT(*)","_id": 0}},
            {"$sort": {"cnt": -1}}
        ]
        documents = self.collection.aggregate(query)
        try:
            value = next(documents)
        except StopIteration:
            return None
        return value['cnt']

    def top_download_books(self, limit: int) -> Iterable[str]:
        query = [
            {"$match": {"action": "bd"}},
            {"$group": {"_id": {"resource": "$resource"}, "COUNT(*)": {"$sum": 1}}},
            {"$project": {"resource": "$_id.resource", "cnt": "$COUNT(*)","_id": 0}},
            {"$sort": {"cnt": -1}},
            {"$limit": limit}
        ]
        documents = self.collection.aggregate(query)
        for document in documents:
            document['book_id'] = document['resource']
            yield document

    def top_viewed_books(self, limit: int) -> Iterable[str]:
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

    def count_download(self, start: datetime, end: datetime)->int:
        query = [
            {"$match": {
                "action": "bd",
                "timestamp": {
                    '$gte': start,
                    '$lt': end
                }
            }
            },
            {"$group": {"_id": {}, "COUNT(*)": {"$sum": 1}}},
            {"$project": {"cnt": "$COUNT(*)","_id": 0}},
            {"$sort": {"cnt": -1}}
        ]
        documents = self.collection.aggregate(query)
        try:
            value = next(documents)
        except StopIteration:
            return 0
        return value['cnt']

    def count_viewed(self, start: datetime, end: datetime)->int:
        query = [
            {"$match": {
                "action": "bv",
                "timestamp": {
                    '$gte': start,
                    '$lt': end
                }
            }
            },
            {"$group": {"_id": {}, "COUNT(*)": {"$sum": 1}}},
            {"$project": {"cnt": "$COUNT(*)","_id": 0}},
            {"$sort": {"cnt": -1}}
        ]
        documents = self.collection.aggregate(query)
        try:
            value = next(documents)
        except StopIteration:
            return 0
        return value['cnt']
