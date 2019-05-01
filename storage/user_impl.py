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

    @classmethod
    def from_bson(cls, document) -> User:
        document['id'] = str(document.pop('_id'))
        return User(**document)

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
        for document in self.collection.find({}):
            yield self.from_bson(document)

    def get_by_login(self, login: str) -> User:
        one_user = self.collection.find_one({'login': login})
        if not one_user:
            raise UserNotFound
        return self.from_bson(one_user)

    def get_count_users(self):
        return self.collection.find({}).count()

    def delete(self, login:str)->bool:
        return self.collection.delete_one({'login': login})
