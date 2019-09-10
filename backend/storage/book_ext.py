import abc
from typing import Iterable
from storage.book import Book, BookDAO


class ExtBook(Book):

    def __init__(self, *args, **kwargs):
        super(ExtBook, self).__init__(*args, **kwargs)
        self.annotation = kwargs.get('annotation', '')


class ExtBookDAO(BookDAO):

    @abc.abstractmethod
    def create(self, card: ExtBook) -> ExtBook:
        pass

    @abc.abstractmethod
    def get_by_id(self, book_id: str) -> ExtBook:
        pass
