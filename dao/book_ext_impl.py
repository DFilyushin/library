from dao.interfaces.book_ext import ExtBook
from dao.book_impl import MongoBookDAO


class MongoExtBookDAO(MongoBookDAO):

    @classmethod
    def from_bson(cls, document) -> ExtBook:
        document['id'] = str(document['filename'])
        return ExtBook(**document)
