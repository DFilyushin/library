class Session(object):

    def __init__(self, session_id: str, login: str, ip: str = '', ttl: int = 0, started: str = ''):
        self.session_id = session_id
        self.login = login
        self.ip = ip
        self.ttl = ttl
        self.started = started