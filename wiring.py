import os
import redis
import rq
from pymongo import MongoClient
from pymongo.database import Database
import dev_settings
import prod_settings
import test_settings
from storage.book import BookDAO
from storage.book_impl import MongoBookDAO
from storage.author_impl import MongoAuthorDAO
from storage.genre_impl import MongoGenreDAO, MongoNewGenreDAO
from storage.version_impl import MongoVersionDAO


class Wiring(object):

    def __init__(self, env=None):
        if env is None:
            env = os.environ.get("FLASK_ENV", "dev")
        self.settings = {
            "dev": dev_settings,
            "prod": prod_settings,
            'test': test_settings
        }[env]

        self.mongo_client = MongoClient(
            host=self.settings.MONGO_HOST,
            port=self.settings.MONGO_PORT)
        self.mongo_database = self.mongo_client[self.settings.MONGO_DATABASE]
        self.book_dao = MongoBookDAO(self.mongo_database)
        self.author_dao = MongoAuthorDAO(self.mongo_database)
        self.genre_dao = MongoNewGenreDAO(self.mongo_database)
        self.library_dao = MongoVersionDAO(self.mongo_database)
        self.redis = redis.StrictRedis(
            host=self.settings.REDIS_HOST,
            port=self.settings.REDIS_PORT,
            db=self.settings.REDIS_DB)
        self.task_queue = rq.Queue(
            name=self.settings.TASK_QUEUE_NAME,
            connection=self.redis)
