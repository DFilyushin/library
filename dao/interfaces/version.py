import abc
from dto.version import LibraryVersion


class LibraryVersionDAO(object, metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def create(self, version: LibraryVersion) -> LibraryVersion:
        pass

    @abc.abstractmethod
    def get_version(self) -> LibraryVersion:
        pass
