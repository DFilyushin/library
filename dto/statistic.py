from datetime import datetime


class Stat(object):

    def __init__(self, ip: str = None, resource: str = None, timestamp: str = None, login: str = None,
                 action: str = None) -> None:
        if not timestamp:
            timestamp = datetime.now()
        self.ip = ip
        self.resource = resource
        self.timestamp = timestamp
        self.login = login
        self.action = action
