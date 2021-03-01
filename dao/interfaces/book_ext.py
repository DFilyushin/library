import abc
from storage.book import BookDAO
from dto.ext_book import ExtBook


class ExtBookDAO(BookDAO):

    @abc.abstractmethod
    def create(self, card: ExtBook) -> ExtBook: pass

    @abc.abstractmethod
    def get_by_id(self, book_id: str) -> ExtBook: pass
