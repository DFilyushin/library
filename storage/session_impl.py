from datetime import datetime
import sys
if sys.version_info[1] >= 6:
    import secrets
else:
    from uuid import uuid4
from storage.session import Session, SessionDAO, SessionNotFound
from redis import StrictRedis
import json


class RedisSessionDAO(SessionDAO):

    def __init__(self, redis: StrictRedis, ttl: int):
        self.redis = redis
        self.default_ttl = ttl

    def create(self, login: str, ip: str)->Session:
        """
        Create session
        :param login: user login
        :param ip: user ip
        :return:
        """
        if sys.version_info[1] >= 6:
            session_id = str(uuid4())
        else:
            session_id = str(uuid4())
        current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        session = Session(session_id, login, ip, self.default_ttl, current_time)
        if self.redis.set(name=session_id, value=json.dumps(session.__dict__)):
            self.redis.expire(session_id, self.default_ttl)
            return session
        else:
            return None

    def update(self, session_id: str)->Session:
        """
        Update session ttl
        :param session_id: session id
        :return: Session object
        """
        session = self.redis.get(session_id)
        if not session:
            return None
        self.redis.expire(session_id, self.default_ttl)
        session_de = json.loads(session)
        return Session(**session_de)

    def get_session_ttl(self, session_id: str)-> int:
        """
        Get session time to live
        :param session_id: session id
        :return:
        """
        if self.redis.exists(session_id):
            return self.redis.ttl(session_id)

    def close(self, session_id: str)->bool:
        """
        Close session
        :param session_id: session id
        :return: True - ok, False - other
        """
        if not self.redis.exists(session_id):
            raise SessionNotFound
        return self.redis.delete(session_id)

    def get_session(self, session_id: str)->Session:
        """
        Get session object by session id
        :param session_id: session id
        :return: Session object
        """
        session = self.redis.get(session_id)
        if not session:
            raise SessionNotFound
        session_de = json.loads(session)
        return Session(**session_de)
