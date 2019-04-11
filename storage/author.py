import abc
from typing import Iterable


class Author(object):

    def __init__(self,
                 id: str = None,
                 first_name: str = None,
                 last_name: str = None,
                 middle_name: str = None
                 ):
        self.id = id
        self.first_name = first_name
        self.last_name = last_name
        self.middle_name = middle_name

    @property
    def name(self):
        result = '{} {} {}'.format(self.last_name, self.first_name, self.middle_name)
        return result


class AuthorDAO(object, metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def create(self, card: Author) -> Author:
        pass

    @abc.abstractmethod
    def update(self, card: Author) -> Author:
        pass

    @abc.abstractmethod
    def get_all(self) -> Iterable[Author]:
        pass

    @abc.abstractmethod
    def get_by_id(self, author_id: str) -> Author:
        pass

    @abc.abstractmethod
    def get_by_last_name(self, last_name: str) -> Iterable[Author]:
        pass

    @abc.abstractmethod
    def get_by_names(self, first_name: str, last_name: str, middle_name: str) -> Iterable[Author]:
        pass

    @abc.abstractmethod
    def get_by_start(self, start_text: str, limit: int, skipped: int):
        pass


class AuthorNotFound(Exception):
    pass
