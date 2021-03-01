import abc
from typing import Iterable
from dto.author import Author


class AuthorDAO(object, metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def create(self, card: Author) -> Author: pass

    @abc.abstractmethod
    def update(self, card: Author) -> Author: pass

    @abc.abstractmethod
    def get_all(self, limit: int, skip: int) -> Iterable[Author]: pass

    @abc.abstractmethod
    def get_by_id(self, author_id: str) -> Author: pass

    @abc.abstractmethod
    def get_by_last_name(self, last_name: str, limit: int, skipped: int) -> Iterable[Author]: pass

    @abc.abstractmethod
    def get_by_names(self, first_name: str, last_name: str, middle_name: str) -> Iterable[Author]: pass

    @abc.abstractmethod
    def get_by_start(self, start_text: str, limit: int, skip: int) -> Iterable[Author]: pass

    @abc.abstractmethod
    def get_count_authors(self): pass


class AuthorNotFound(Exception):
    pass
