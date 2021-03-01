import abc
from typing import Iterable
from dto.user import User


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
    def delete(self, login: str) -> bool:
        pass


class UserNotFound(Exception):
    pass


class UserExists(Exception):
    pass
