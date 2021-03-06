import abc
from typing import Iterable


class Genre(object):

    def __init__(self,
                 id: str = None,
                 parent: str = None,
                 titles: list = None,
                 detailed: list = None,
                 sub_genres: list = None):
        self.id = id
        self.parent = parent
        self.titles = titles
        self.detailed = detailed
        self.sub_genres = sub_genres


class GenreDAO(object, metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def create(self, genre: Genre) -> Genre:
        pass

    @abc.abstractmethod
    def update(self, genre: Genre)-> Genre:
        pass

    @abc.abstractmethod
    def get_all(self) -> Iterable[Genre]:
        pass

    @abc.abstractmethod
    def get_by_id(self, genre_id: str) -> Genre:
        pass


class GenreNotFound(Exception):
    pass
