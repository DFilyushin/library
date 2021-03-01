class Book(object):
    def __init__(
            self,
            **kwargs

    ):
        self.id = kwargs.get('id', '')
        self.name = kwargs.get('name', '')
        self.authors = kwargs.get('authors', '')
        self.series = kwargs.get('series', '')
        self.sernum = kwargs.get('sernum', '')
        self.filename = kwargs.get('filename', '')
        self.deleted = kwargs.get('deleted', '')
        self.lang = kwargs.get('lang', '')
        self.keywords = kwargs.get('keywords', '')
        self.added = kwargs.get('added', '')
        self.genres = kwargs.get('genres', '')
        self.year = kwargs.get('year', '')
        self.isbn = kwargs.get('isbn', '')
        self.city = kwargs.get('city', '')
        self.pub_name = kwargs.get('pub_name', '')
        self.publisher = kwargs.get('publisher', '')
        self.height = kwargs.get('height', '')
        self.width = kwargs.get('width', '')