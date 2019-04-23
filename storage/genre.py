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


class NewGenre(object):

    def __init__(self, id: str = None, parent: str = None, titles: list = None, detailed: list = None, sub_genres: list = None, count_books: int = 0):
        self.id = id
        self.parent = parent
        self.titles = titles
        self.detailed = detailed
        self.sub_genres = sub_genres
        self.count_books = count_books


class NewGenreDAO(object, metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def create(self, genre: NewGenre) -> NewGenre:
        pass

    @abc.abstractmethod
    def update(self, genre: NewGenre)-> NewGenre:
        pass

    @abc.abstractmethod
    def get_all(self) -> Iterable[NewGenre]:
        pass

    @abc.abstractmethod
    def get_by_id(self, genre_id: str) -> NewGenre:
        pass


class GenreNotFound(Exception):
    pass
