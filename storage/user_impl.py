from typing import Iterable
import bson
import bson.errors
from pymongo.collection import Collection
from pymongo.database import Database
from pymongo import ASCENDING
from pymongo.errors import DuplicateKeyError
from storage.user import User, UserDAO, UserNotFound, UserExists


class MongoUserDAO(UserDAO):

    def __init__(self, mongo_database: Database):
        self.database = mongo_database
        self.collection.create_index(
            [("login", ASCENDING)],
            unique=True
        )

    @property
    def collection(self) -> Collection:
        return self.database['users']

    @classmethod
    def to_bson(cls, user: User):
        result = {
            k: v
            for k, v in user.__dict__.items() if v is not None
        }
        if 'id' in result:
            result['_id'] = bson.ObjectId(result.pop('id'))
        return result

    def create(self, user: User) -> User:
        try:
            one_user = self.collection.insert_one(self.to_bson(user))
        except DuplicateKeyError:
            raise UserExists
        user.id = str(one_user.inserted_id)
        return user

    def update(self, user: User) -> User:
        pass

    def get_all(self) -> Iterable[User]:
        pass

    def get_by_login(self, login: str) -> User:
        pass

    def get_count_users(self):
        return self.collection.find({}).count()
