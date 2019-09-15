import os
import redis
from pymongo import MongoClient
from pymongo.database import Database
import dev_settings
import prod_settings
import test_settings
import docker_settings
from storage.book_impl import MongoBookDAO
from storage.author_impl import MongoAuthorDAO
from storage.genre_impl import MongoGenreDAO
from storage.version_impl import MongoVersionDAO
from storage.language_impl import MongoLanguageDAO
from tools.book_store import BookStore
from storage.stat_impl import MongoStatDAO
from storage.user_impl import MongoUserDAO
from storage.group_impl import MongoGroupDAO
from api_cache import AppCache
from storage.session_impl import RedisSessionDAO
from storage.starred_book_impl import MongoStarredBook
from storage.book_ext_impl import MongoExtBookDAO


class Wiring(object):

    def __init__(self, env=None):
        if env is None:
            env = os.environ.get("FLASK_ENV", "dev")
        self.settings = {
            "dev": dev_settings,
            "prod": prod_settings,
            "test": test_settings,
            "docker": docker_settings
        }[env]

        print('Mongo base: {}:{}:{}'.format(os.environ.get('MONGO_HOST'), os.environ.get('MONGO_PORT'), os.environ.get('MONGO_DATABASE')))

        self.cache_db = AppCache(
            self.settings.REDIS_HOST,
            self.settings.REDIS_PORT,
            self.settings.REDIS_CACHE_DB,
            self.settings.CACHE_DEFAULT_TIMEOUT)
        self.session_db = redis.StrictRedis(
            self.settings.REDIS_HOST,
            self.settings.REDIS_PORT,
            self.settings.REDIS_CACHE_DB
        )
        self.use_sessions = self.settings.USE_SESSIONS
        self.mongo_client = MongoClient(
            host=self.settings.MONGO_HOST,
            port=self.settings.MONGO_PORT)
        self.mongo_client = MongoClient(
            host=self.settings.MONGO_HOST,
            port=self.settings.MONGO_PORT
        )
        self.mongo_database = self.mongo_client[self.settings.MONGO_DATABASE]
        self.book_dao = MongoBookDAO(self.mongo_database)
        self.book_ext_dao = MongoExtBookDAO(self.mongo_database)
        self.author_dao = MongoAuthorDAO(self.mongo_database)
        self.genre_dao = MongoGenreDAO(self.mongo_database)
        self.library_dao = MongoVersionDAO(self.mongo_database)
        self.language_dao = MongoLanguageDAO(self.mongo_database)
        self.book_store = BookStore(self.settings.LIB_ARCHIVE, self.settings.TMP_DIR, self.settings.THUMBNAIL_SIZE)
        self.stat = MongoStatDAO(self.mongo_database)
        self.users = MongoUserDAO(self.mongo_database)
        self.sessions = RedisSessionDAO(self.session_db, self.settings.DEFAULT_SESSION_TTL)
        self.stars = MongoStarredBook(self.mongo_database)
        self.groups = MongoGroupDAO(self.mongo_database)
