from datetime import datetime


class StarredBook(object):

    def __init__(self, id: str = None, login: str = None, book_id: str = None, added: str = None):
        self.id = id
        self.login = login
        self.book_id = book_id
        if not added:
            added = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.added = added