import abc
from typing import Iterable
from dto.genre import Genre


class GenreDAO(object, metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def create(self, genre: Genre) -> Genre:
        pass

    @abc.abstractmethod
    def update(self, genre: Genre) -> Genre:
        pass

    @abc.abstractmethod
    def get_all(self) -> Iterable[Genre]:
        pass

    @abc.abstractmethod
    def get_by_id(self, genre_id: str) -> Genre:
        pass


class GenreNotFound(Exception):
    pass
