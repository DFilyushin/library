import abc
from typing import Iterable


class Book(object):
    def __init__(
            self,
            **kwargs

    ):
        self.id = kwargs.get('id', '')
        self.name = kwargs.get('name', '')
        self.authors = kwargs.get('authors', '')
        self.series = kwargs.get('series', '')
        self.sernum = kwargs.get('sernum', '')
        self.filename = kwargs.get('filename', '')
        self.deleted = kwargs.get('deleted', '')
        self.lang = kwargs.get('lang', '')
        self.keywords = kwargs.get('keywords', '')
        self.added = kwargs.get('added', '')
        self.genres = kwargs.get('genres', '')
        self.year = kwargs.get('year', '')
        self.isbn = kwargs.get('isbn', '')
        self.city = kwargs.get('city', '')
        self.pub_name = kwargs.get('pub_name', '')
        self.publisher = kwargs.get('publisher', '')
        self.height = kwargs.get('height', '')
        self.width = kwargs.get('width', '')


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

    @abc.abstractmethod
    def search_book(self, name: str, lang: str, series: str, keyword: str):
        pass

    @abc.abstractmethod
    def books_by_genres(self, genre: str):
        pass

    @abc.abstractmethod
    def get_count_books(self):
        pass

    @abc.abstractmethod
    def get_genres_by_author(self, id: str):
        pass

    @abc.abstractmethod
    def get_book_by_filename(self, filename: str):
        pass

    @abc.abstractmethod
    def get_popular_books(self, limit: int):
        pass


class BookNotFound(Exception):
    pass
