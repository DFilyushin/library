from dto.book import Book


class ExtBook(Book):

    def __init__(self, *args, **kwargs):
        super(ExtBook, self).__init__(*args, **kwargs)
        self.annotation = kwargs.get('annotation', '')
