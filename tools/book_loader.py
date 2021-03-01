import os
import io
import bson
from datetime import datetime
from time import time
from wiring import Wiring
from dto.book import Book
from dto.author import Author
from dao.interfaces.author import AuthorNotFound


class BookLoader(object):
    """
    Book loader from index files
    """

    def __init__(self, wiring: Wiring):
        self.wiring = wiring
        self.path = self.wiring.settings.LIB_INDEXES

    def get_files(self):
        for file in filter(lambda x: x.endswith('.inp'), os.listdir(self.path)):
            t0 = time()
            yield os.path.join(self.path, file)
            print('File {} processed by {}'.format(file, time()-t0))

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
        count_lines = 0
        count_new = 0
        for line in lines:
            count_lines += 1
            book_item = line.split(chr(4))
            keywords_list = []
            keywords = book_item[13]
            if keywords:
                keywords_list = keywords.split(',')
            authors = self.get_authors(book_item[0])  # get author keys
            genres = book_item[1].split(':')[:-1]  # get genres

            # Check if book exists by filename

            exists_book = self.wiring.book_dao._get_by_id(book_item[5])
            if exists_book:
                exists_book.authors = authors
                self.wiring.book_dao.update(exists_book)
                continue

            book = Book(
                    name=book_item[2],
                    authors=authors,
                    series=book_item[3],
                    sernum=book_item[4],
                    filename=book_item[5],
                    deleted=book_item[8] == '1',
                    lang=book_item[11],
                    keywords=keywords_list,
                    added=book_item[10],
                    genres=genres
                )
            books.append(book)
            count_new += 1
            if len(books) > 100:
                self.wiring.book_dao.create_many(books)
                books = []
        if books:
            self.wiring.book_dao.create_many(books)
        return count_lines, count_new

    def process(self):
        print('{}: Import books, authors from index files...'.format(datetime.now()))
        files = self.get_files()
        book_lines = self.get_file_bookline(files)
        all, new = self.process_line(book_lines)
        print('All books: {}\nNew book: {}'.format(all, new))
        print('{}: Done'.format(datetime.now()))


if __name__ == '__main__':
    wiring = Wiring()
    loader = BookLoader(wiring)
    loader.process()
