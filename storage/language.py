import abc
from typing import Iterable


class Language(object):

    def __init__(self, id: str = None, ext: str = None, name: str = None):
        self.id = id
        self.ext = ext
        self.name = name


class LanguageDAO(object, metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def create(self, language: Language) -> Language:
        pass

    @abc.abstractmethod
    def update(self, language: Language) -> Language:
        pass

    @abc.abstractmethod
    def get_all(self) -> Iterable[Language]:
        pass

    @abc.abstractmethod
    def get_by_id(self, language_id: str) -> Language:
        pass


class LanguageNotFound(Exception):
    pass

class LanguageExists(Exception):
    pass