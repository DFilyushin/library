import os
import redis
import rq
from motor.motor_asyncio import AsyncIOMotorClient as MongoClient
import dev_settings
import prod_settings
from storage.book import BookDAO
from storage.book_motor import MotorBookDAO


class Wiring(object):

    def __init__(self, env=None):
        if env is None:
            env = os.environ.get("APP_ENV", "dev")
        self.settings = {
            "dev": dev_settings,
            "prod": prod_settings,
        }[env]

        # С ростом числа компонент этот код будет усложняться.
        # В будущем вы можете сделать тут такой DI, какой захотите.
        self.mongo_client = MongoClient(
            host=self.settings.MONGO_HOST,
            port=self.settings.MONGO_PORT)
        self.mongo_database = self.mongo_client[self.settings.MONGO_DATABASE]
        self.card_dao = MotorBookDAO(self.mongo_database)
        self.redis = redis.StrictRedis(
            host=self.settings.REDIS_HOST,
            port=self.settings.REDIS_PORT,
            db=self.settings.REDIS_DB)
        self.task_queue = rq.Queue(
            name=self.settings.TASK_QUEUE_NAME,
            connection=self.redis)


