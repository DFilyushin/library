"""
Library test settings
"""

# library settings

LIB_INDEXES = r'd:/librusec/index'
LIB_ARCHIVE = r'c:/librusec'
TMP_DIR = r'c:/temp'

# default limits for rows
DEFAULT_LIMITS = 20

# default skip
DEFAULT_SKIP_RECORD = 0

# mongo settings
MONGO_HOST = "localhost"
MONGO_PORT = 27017
MONGO_DATABASE = "books_test"

# redis-cache settings
REDIS_HOST = "localhost"
REDIS_PORT = 6379

# redis base for cache
REDIS_SESSION_DB = 2

# redis base for sessions
REDIS_CACHE_DB = 1

# expire cache time
CACHE_DEFAULT_TIMEOUT = 43200

# name of queue for tasks
TASK_QUEUE_NAME = "btasks"

# minimal size for resize books covers
THUMBNAIL_SIZE = 200, 200