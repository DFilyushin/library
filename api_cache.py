import redis


class AppCache(object):
    """
    Cache for application
    """

    def __init__(self, host: str, port: int, db_num: int, store_seconds: int):
        self.db_num = db_num
        self.host = host
        self.port = port
        self.conn = redis.StrictRedis(self.host, self.port, db_num)
        self.default_timeout = store_seconds

    def set_value(self, name: str, value: str, expire: int = None):
        result = self.conn.set(name=name, value=value)
        if not expire:
            expire = self.default_timeout
        if result:
            self.conn.expire(name=name, time=expire)

    def get_value(self, name: str):
        return self.conn.get(name)
