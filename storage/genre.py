import abc
from typing import Iterable


class Genre(object):

    def __init__(self, id: str = None, slug: str = None, name: str = None):
        self.id = id
        self.slug = slug
        self.name = name


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

    @abc.abstractmethod
    def get_by_slug(self, slug: str) -> Genre:
        pass


class GenreNotFound(Exception):
    pass
