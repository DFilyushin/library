import abc
from typing import Iterable
from datetime import datetime


class StarredBook(object):

    def __init__(self, id: str = None, login: str = None, book_id: str = None, added: str = None):
        self.id = id
        self.login = login
        self.book_id = book_id
        if not added:
            added = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.added = added


class StarredBookDAO(object, metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def create(self, star: StarredBook)->StarredBook:
        pass

    @abc.abstractmethod
    def get_by_id(self, star_id: str)->StarredBook:
        pass

    @abc.abstractmethod
    def get_by_login(self, login: str)->Iterable[StarredBook]:
        pass

    @abc.abstractmethod
    def get_by_book(self, book_id: str)->Iterable[StarredBook]:
        pass

    @abc.abstractmethod
    def delete(self, id: str)->bool:
        pass

    @abc.abstractmethod
    def delete_by_login(self, login:str)->bool:
        pass

    @abc.abstractmethod
    def delete_by_book(self, book_id:str)->bool:
        pass

    @abc.abstractmethod
    def delete_by_star_pair(self, login: str, book_id: str) -> bool:
        pass

class StarExists(Exception):
    pass
