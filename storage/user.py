import abc
from typing import Iterable


class User(object):

    def __init__(self,
                 id: str = None,
                 login: str = None,
                 password: str = None,
                 group: str = 'default'
                 ):
        self.id = id
        self.login = login
        self.password = password
        self.group = group


class UserDAO(object, metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def create(self, user: User) -> User:
        pass

    @abc.abstractmethod
    def update(self, user: User) -> User:
        pass

    @abc.abstractmethod
    def get_all(self) -> Iterable[User]:
        pass

    @abc.abstractmethod
    def get_by_login(self, login: str) -> User:
        pass

    @abc.abstractmethod
    def get_count_users(self):
        pass

    @abc.abstractmethod
    def delete(self, login:str)->bool:
        pass


class UserNotFound(Exception):
    pass


class UserExists(Exception):
    pass
