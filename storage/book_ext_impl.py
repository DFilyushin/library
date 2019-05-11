from storage.book_ext import ExtBook
from storage.book_impl import MongoBookDAO


class MongoExtBookDAO(MongoBookDAO):

    @classmethod
    def from_bson(cls, document) -> ExtBook:
        document['id'] = str(document['filename'])
        return ExtBook(**document)
