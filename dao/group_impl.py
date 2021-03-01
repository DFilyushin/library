from typing import Iterable
import bson
import bson.errors
from pymongo.collection import Collection
from pymongo.database import Database
from pymongo import ASCENDING
from pymongo.errors import DuplicateKeyError
from dao.interfaces.group import Group, GroupDAO, GroupNotFound, GroupExist
from dao.interfaces.user import User, UserDAO
from dao.user_impl import MongoUserDAO


class MongoGroupDAO(GroupDAO):

    def __init__(self, mongo_database: Database):
        self.database = mongo_database
        self.collection.create_index(
            [("name", ASCENDING)],
            unique=True
        )

    @property
    def collection(self) -> Collection:
        return self.database['groups']

    @classmethod
    def to_bson(cls, group: Group):
        result = {
            k: v
            for k, v in group.__dict__.items() if v is not None
        }
        if 'id' in result:
            result['_id'] = bson.ObjectId(result.pop('id'))
        return result

    @classmethod
    def from_bson(cls, document) -> Group:
        document['id'] = str(document.pop('_id'))
        return Group(**document)

    def create(self, group: Group)->Group:
        try:
            one_group = self.collection.insert_one(self.to_bson(group))
        except DuplicateKeyError:
            raise GroupExist
        group.id = str(one_group.inserted_id)
        return group

    def get_by_name(self, name: str)->Group:
        document = self.collection.find_one({'name': name})
        if not document:
            raise GroupNotFound
        return self.from_bson(document)

    def update(self, group: Group)->Group:
        if self.collection.update_one({'name': group.name}, {'$set': {'limit_per_day': group.limit_per_day}}):
            return group
        else:
            return None

    def get_all(self)->Iterable[Group]:
        documents = self.collection.find({})
        for document in documents:
            yield self.from_bson(document)

    def get_users(self, group: str)->Iterable[User]:
        user = MongoUserDAO(self.database)
        documents = user.collection.find({'group': group})
        for document in documents:
            yield self.from_bson(document)

    def delete(self, group: Group):
        return self.collection.delete_one({'name': group.name})
