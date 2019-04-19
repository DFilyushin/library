from storage.book import Book, BookNotFound
from storage.author import Author, AuthorNotFound
from storage.genre import Genre, NewGenre
from storage.version import LibraryVersion
from storage.language import Language
from wiring import Wiring
import io
import bson
import xml.etree.ElementTree as ET
from datetime import datetime

# from wiring_motor import Wiring

import os
from time import time


class LanguageLoader(object):
    """
    Fb2 language loader
    """

    def __init__(self):
        self.wiring = Wiring()

    def process_file(self, filename):
        with io.open(filename, encoding='utf-8') as file:
            for line in file:
                yield line

    def process_line(self, lines):
        for line in lines:
            lang_list = line.split(';')
            language = Language(
                id=lang_list[1],
                ext=lang_list[0],
                name=lang_list[2].rstrip()
            )
            try:
                self.wiring.language_dao.create(language)
            except Exception as E:
                print('Line {} is skipped cause error {}'.format(line, str(E)))

    def process(self):
        path = os.path.join(self.wiring.settings.LIB_INDEXES, 'language.txt')
        lines = self.process_file(path)
        self.process_line(lines)


class GenreLoader(object):
    """
    Fb2 genre loader
    """

    def __init__(self):
        self.wiring = Wiring()

    def process_file(self, filename):
        print(filename)
        with io.open(filename, encoding='utf-8') as file:
            for line in file:
                yield line

    def process_line(self, lines):
        for line in lines:
            genre_list = line.split(';')
            genre = Genre(
                slug=genre_list[0],
                name=genre_list[1].rstrip()
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


class NewGenreLoader(object):
    def __init__(self):
        self.wiring = Wiring()
        self.genres = dict()

    def get_subgenre(self, node, parent_name):
        for subgenre in node.getchildren():
            item = dict()
            item['parent'] = parent_name
            item['name'] = subgenre.get('value')
            item['title'] = []
            item['detailed'] = []
            for sg_item in subgenre.getchildren():
                if sg_item.tag == 'genre-descr':
                    item['title'].append({sg_item.get('lang'): sg_item.get('title')})
                elif sg_item.tag == 'genre-alt':
                    item2 = dict()
                    item2['parent'] = parent_name
                    item2['name'] = sg_item.get('value')
                    item2['title'] = item['title']
                    item2['detailed'] = []
                    if not self.genres.get(sg_item.get('value')):
                        self.genres[sg_item.get('value')]=item2
                    else:
                        print('{} skipped 1'.format(sg_item.get('value')))
            if not self.genres.get(item['name']):
                self.genres[item['name']] = item
            else:
                print('{} skipped 2'.format(item['name']))

    def process(self):
        path = os.path.join(self.wiring.settings.LIB_INDEXES, 'genres.xml')
        root = ET.parse(path).getroot()
        for appt in root.getchildren():  # genre
            genre_item = dict()
            genre_item['name'] = appt.get('value')
            genre_item['parent'] = ''
            genre_item['title'] = []
            genre_item['detailed'] = []
            for elem in appt.getchildren():
                if elem.tag == 'subgenres':
                    self.get_subgenre(elem, genre_item['name'])
                elif elem.tag == 'root-descr':
                    genre_item['title'].append({elem.get('lang'): elem.get('genre-title')})
                    genre_item['detailed'].append({elem.get('lang'): elem.get('detailed')})
            self.genres[appt.get('value')] = genre_item

        for key, item in self.genres.items():
            genre = NewGenre(
                id=item['name'],
                parent=item['parent'],
                titles=item['title'],
                detailed=item['detailed']
            )
            try:
                self.wiring.genre_dao.create(genre)
            except Exception as E:
                print('Item {} is skipped cause error {}'.format(item['name'], str(E)))


def update_version():
    wiring = Wiring()
    path = os.path.join(wiring.settings.LIB_INDEXES, 'version.info')
    with io.open(path) as file:
        num_version = file.read()

    version = LibraryVersion(
        version=num_version.rstrip(),
        added=datetime.now().strftime('%Y%m%d')
    )
    wiring.library_dao.create(version)


if __name__ == '__main__':

    lang_loader = LanguageLoader()
    lang_loader.process()

    exit()

    book_loader = BookLoader()
    book_loader.process()

    gl = GenreLoader()
    gl.process()

    new_genre = NewGenreLoader()
    new_genre.process()

    update_version()
