import abc
from dto.session import Session


class SessionDAO(object, metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def create(self, login: str, ip: str, ) -> Session:
        pass

    @abc.abstractmethod
    def update(self, session_id: str) -> Session:
        pass

    @abc.abstractmethod
    def close(self, session_id: str) -> bool:
        pass

    @abc.abstractmethod
    def get_session(self, session_id: str) -> Session:
        pass


class SessionNotFound(Exception):
    pass
