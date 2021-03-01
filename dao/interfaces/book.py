import abc
from typing import Iterable
from dto.book import Book


class BookDAO(object, metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def create(self, card: Book) -> Book: pass

    @abc.abstractmethod
    def update(self, card: Book) -> Book: pass

    @abc.abstractmethod
    def get_all(self) -> Iterable[Book]: pass

    @abc.abstractmethod
    def get_by_id(self, book_id: str) -> Book: pass

    @abc.abstractmethod
    def get_by_author(self, author: str) -> Iterable[Book]: pass

    @abc.abstractmethod
    def get_by_name(self, name: str) -> Book: pass

    @abc.abstractmethod
    def search_book(self, name: str, lang: str, series: str, keyword: str): pass

    @abc.abstractmethod
    def books_by_genres(self, genre: str): pass

    @abc.abstractmethod
    def get_count_books(self): pass

    @abc.abstractmethod
    def get_genres_by_author(self, id: str): pass

    @abc.abstractmethod
    def get_book_by_filename(self, filename: str): pass

    @abc.abstractmethod
    def get_popular_books(self, limit: int): pass


class BookNotFound(Exception):
    pass
