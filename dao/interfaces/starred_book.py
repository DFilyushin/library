import abc
from typing import Iterable
from dto.starred_book import StarredBook


class StarredBookDAO(object, metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def create(self, star: StarredBook) -> StarredBook:
        pass

    @abc.abstractmethod
    def get_by_id(self, star_id: str) -> StarredBook:
        pass

    @abc.abstractmethod
    def get_by_login(self, login: str) -> Iterable[StarredBook]:
        pass

    @abc.abstractmethod
    def get_by_book(self, book_id: str) -> Iterable[StarredBook]:
        pass

    @abc.abstractmethod
    def delete(self, id: str) -> bool:
        pass

    @abc.abstractmethod
    def delete_by_login(self, login: str) -> bool:
        pass

    @abc.abstractmethod
    def delete_by_book(self, book_id: str) -> bool:
        pass

    @abc.abstractmethod
    def delete_by_star_pair(self, login: str, book_id: str) -> bool:
        pass


class StarExists(Exception):
    pass
