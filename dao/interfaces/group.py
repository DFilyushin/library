import abc
from typing import Iterable
from storage.user import User
from dto.group import Group


class GroupDAO(object, metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def create(self, group: Group) -> Group:
        pass

    @abc.abstractmethod
    def update(self, group: Group) -> Group:
        pass

    @abc.abstractmethod
    def get_by_name(self, name: str) -> Group:
        pass

    @abc.abstractmethod
    def get_all(self)->Iterable[Group]:
        pass

    @abc.abstractmethod
    def get_users(self, group: str) -> Iterable[User]:
        pass

    @abc.abstractmethod
    def delete(self, group: Group):
        pass


class GroupNotFound(Exception):
    pass


class GroupExist(Exception):
    pass
