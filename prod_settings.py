"""
Library production settings
"""

LIB_INDEXES = r'path/to/librusec/index'
LIB_ARCHIVE = r'path/to/librusec/library'
TMP_DIR = r'/path/to/tmp/directory'

# mongo settings
MONGO_HOST = "localhost"
MONGO_PORT = 27017
MONGO_DATABASE = "books"

# redis-cache settings
REDIS_HOST = "localhost"
REDIS_PORT = 6379

# redis base for sessions
REDIS_CACHE_DB = 1

# redis base for cache
REDIS_SESSION_DB = 2

# expire cache time
CACHE_DEFAULT_TIMEOUT = 43200

# name of queue for tasks
TASK_QUEUE_NAME = "btasks"

# minimal size for resize books covers
THUMBNAIL_SIZE = 200, 200

