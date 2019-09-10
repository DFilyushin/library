import abc


class Session(object):

    def __init__(self, session_id: str, login: str, ip: str = '', ttl: int = 0, started: str = ''):
        self.session_id = session_id
        self.login = login
        self.ip = ip
        self.ttl = ttl
        self.started = started


class SessionDAO(object, metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def create(self, login: str, ip: str, )->Session:
        pass

    @abc.abstractmethod
    def update(self, session_id: str)->Session:
        pass

    @abc.abstractmethod
    def close(self, session_id: str)->bool:
        pass

    @abc.abstractmethod
    def get_session(self, session_id: str)->Session:
        pass


class SessionNotFound(Exception):
    pass