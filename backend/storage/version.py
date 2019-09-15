import abc


class LibraryVersion(object):

    def __init__(self, id: str = None, version: str = 'Not found', added: str = ''):
        self.id = id
        self.version = version
        self.added = added


class LibraryVersionDAO(object, metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def create(self, version: LibraryVersion)->LibraryVersion:
        pass

    @abc.abstractmethod
    def get_version(self)->LibraryVersion:
        pass


class VersionNotFound(Exception):
    pass
