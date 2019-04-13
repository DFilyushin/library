from storage.book import Book, BookNotFound
from storage.author import Author, AuthorNotFound
from storage.genre import Genre
from wiring import Wiring
import io
import bson
# from wiring_motor import Wiring

import os
from time import time


class GenreLoader(object):
    """
    Fb2 genre loader
    """

    def __init__(self):
        self.wiring = Wiring()

    def process_file(self, filename):
        # with open(filename, 'rb') as file:
        print(filename)
        with io.open(filename, encoding='utf-8') as file:
            for line in file:
                yield line

    def process_line(self, lines):
        for line in lines:
            genre_list = line.split(';')
            genre = Genre(
                slug=genre_list[0],
                name=genre_list[1]
            )
            try:
                self.wiring.genre_dao.create(genre)
            except Exception as E:
                print('Line {} is skipped cause error {}'.format(line, str(E)))

    def process(self):
        path = os.path.join(self.wiring.settings.LIB_INDEXES, 'genres.txt')
        lines = self.process_file(path)
        self.process_line(lines)


class BookLoader(object):
    """
    Book loader from index files
    """

    def __init__(self):
        self.wiring = Wiring()

    def get_files(self):
        path = self.wiring.settings.LIB_INDEXES
        for file in filter(lambda x: x.endswith('.inp'), os.listdir(path)):
            t0 = time()
            yield os.path.join(path, file)
            print(file, time()-t0)

    def get_file_bookline(self, files):
        for filename in files:
            with io.open(filename, encoding='utf-8') as file:
                for line in file:
                    yield line

    def get_authors(self, author_list):
        result = []
        for item in author_list.split(':')[:-1]:
            authors = item.split(',')
            if len(authors) < 3:
                for i in range(3 - len(authors)):
                    authors.append('')
            first_name = authors[1]
            last_name = authors[0]
            middle_name = authors[2]
            try:
                author = self.wiring.author_dao.get_by_names(first_name, last_name, middle_name)
            except AuthorNotFound:
                author = self.wiring.author_dao.create(
                    Author(
                        first_name=first_name,
                        last_name=last_name,
                        middle_name=middle_name
                    )
                )
            result.append(bson.ObjectId(author.id))
        return result

    def process_line(self, lines):
        # AUTHOR;GENRE;TITLE;SERIES;SERNO;FILE;SIZE;LIBID;DEL;EXT;DATE;LANG;LIBRATE;KEYWORDS;
        #   0   ;  1  ;  2  ;  3   ;  4  ; 5  ; 6  ;  7  ; 8 ; 9 ; 10 ; 11 ;   12  ;   13   ;
        books = []
        for line in lines:
            book_item = line.split(chr(4))
            keywords_list = []
            keywords = book_item[13]
            if keywords:
                keywords_list = keywords.split(',')
            authors = self.get_authors(book_item[0])  # get author keys
            genres = book_item[1].split(':')[:-1] # get genres
            book = Book(
                    # slug=book_item[5],
                    name=book_item[2],
                    authors=authors,
                    series=book_item[3],
                    sernum=book_item[4],
                    filename=book_item[5],
                    deleted=book_item[8],
                    lang=book_item[11],
                    keywords=keywords_list,
                    added=book_item[10],
                    genres=genres
                )
            books.append(book)
            if len(books) > 100:
                self.wiring.book_dao.create_many(books)
                books = []
            # self.wiring.card_dao.create(book)
        if books:
            self.wiring.book_dao.create_many(books)

    def process(self):
        files = self.get_files()
        book_lines = self.get_file_bookline(files)
        self.process_line(book_lines)


book_loader = BookLoader()
book_loader.process()

# gl = GenreLoader()
# gl.process()
