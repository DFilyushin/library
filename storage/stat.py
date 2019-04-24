import abc
from typing import Iterable
from datetime import datetime

class Stat(object):

    def __init__(self, ip: str = None, resource: str = None, timestamp: str = None):
        if not timestamp:
            timestamp = datetime.now()
        self.ip = ip
        self.resource = resource
        self.timestamp = timestamp


class StatDAO(object, metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def create(self, stat: Stat) -> Stat:
        pass

    @abc.abstractmethod
    def stat_by_resource(self, resource: str, start: str, end: str) -> Iterable[dict]:
        pass

    @abc.abstractmethod
    def stat_by_ip(self, ip: str, start: str, end: str) -> Iterable[dict]:
        pass

    @abc.abstractmethod
    def stat_by_period(self, start: str, end: str) -> Iterable[Stat]:
        pass
