import abc
from typing import Iterable
from storage.user import User


class Group(object):

    def __init__(self, id: str = None, name: str = None, limit_per_day: int = 0):
        self.id = id
        self.name = name
        self.limit_per_day = limit_per_day


class GroupDAO(object, metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def create(self, group: Group)->Group:
        pass

    @abc.abstractmethod
    def update(self, group: Group)->Group:
        pass

    @abc.abstractmethod
    def get_by_name(self, name: str)->Group:
        pass

    @abc.abstractmethod
    def get_all(self)->Iterable[Group]:
        pass

    @abc.abstractmethod
    def get_users(self, group: str)->Iterable[User]:
        pass

    @abc.abstractmethod
    def delete(self, group: Group):
        pass


class GroupNotFound(Exception):
    pass


class GroupExist(Exception):
    pass
