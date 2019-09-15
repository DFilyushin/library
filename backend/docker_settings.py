import os

# dir for library index
SETTINGS_ = """
Library development settings
"""
LIB_INDEXES = os.environ.get('LIB_INDEX')

# dir for zips
LIB_ARCHIVE = os.environ.get('LIB_ARCHIVE')

# tmp dir for zip, fb2
TMP_DIR = os.environ.get('TMP_DIR')

# dir for images
IMAGE_DIR = os.environ.get('IMAGE_DIR')

# default limits for rows
DEFAULT_LIMITS = 20

# default skip
DEFAULT_SKIP_RECORD = 0

# mongo settings
MONGO_HOST = os.environ.get('MONGO_HOST')
MONGO_PORT = int(os.environ.get('MONGO_PORT', 27017))
MONGO_DATABASE = os.environ.get('MONGO_DATABASE')

# redis-cache settings
REDIS_HOST = os.environ.get('REDIS_HOST')
REDIS_PORT = int(os.environ.get('REDIS_PORT', 6379))

# redis base for cache
REDIS_SESSION_DB = 2

# default session ttl
DEFAULT_SESSION_TTL = 300  # seconds

# redis base for sessions
REDIS_CACHE_DB = 1

# expire cache time
CACHE_DEFAULT_TIMEOUT = 43200

# name of queue for tasks
TASK_QUEUE_NAME = "btasks"

# minimal size for resize books covers
THUMBNAIL_SIZE = 200, 200

# Use session now?
USE_SESSIONS = False

# Avalaible formats for books
FORMATS = ('zip', 'fb2')
