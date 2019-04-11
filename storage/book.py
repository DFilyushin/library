import abc
from typing import Iterable


class Book(object):
    def __init__(
            self,
            id: str = None,
            slug: str = None,
            name: str = None,
            authors: list = None,
            series: str = None,
            sernum: int = None,
            filename: str = None,
            deleted: bool = False,
            lang: str = None,
            keywords: list = None,
            added: str = None,
            genres: list =None
    ):
        self.id = id
        self.slug = slug
        self.name = name
        self.authors = authors
        self.series = series
        self.sernum = sernum
        self.filename = filename
        self.deleted = deleted
        self.lang = lang
        self.keywords = keywords
        self.added = added
        self.genres = genres



class BookDAO(object, metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def create(self, card: Book) -> Book:
        pass

    @abc.abstractmethod
    def update(self, card: Book) -> Book:
        pass

    @abc.abstractmethod
    def get_all(self) -> Iterable[Book]:
        pass

    @abc.abstractmethod
    def get_by_id(self, book_id: str) -> Book:
        pass

    @abc.abstractmethod
    def get_by_author(self, author: str) -> Iterable[Book]:
        pass

    @abc.abstractmethod
    def get_by_name(self, name: str) -> Book:
        pass


class BookNotFound(Exception):
    pass
