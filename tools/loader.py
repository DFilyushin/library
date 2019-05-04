import io
import bson
import re
import xml.etree.ElementTree as ET
from datetime import datetime

from storage.book import Book, BookNotFound
from storage.author import Author, AuthorNotFound
from storage.genre import Genre
from storage.version import LibraryVersion
from storage.language import Language
from storage.group import Group
from wiring import Wiring

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
            item['title'] = dict()
            item['detailed'] = dict()
            for sg_item in subgenre.getchildren():
                if sg_item.tag == 'genre-descr':
                    lang = sg_item.get('lang')
                    lang_title = sg_item.get('title')
                    item['title'][lang] = lang_title
                elif sg_item.tag == 'genre-alt':
                    item2 = dict()
                    item2['parent'] = parent_name
                    item2['name'] = sg_item.get('value')
                    item2['title'] = item['title']
                    item2['detailed'] = dict()
                    if not self.genres.get(sg_item.get('value')):
                        self.genres[sg_item.get('value')] = item2
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
            genre_item['title'] = dict()
            genre_item['detailed'] = dict()
            for elem in appt.getchildren():
                if elem.tag == 'subgenres':
                    self.get_subgenre(elem, genre_item['name'])
                elif elem.tag == 'root-descr':
                    lang = elem.get('lang')
                    lang_title = elem.get('genre-title')
                    genre_item['title'][lang] = lang_title
                    genre_item['detailed'][elem.get('lang')] = elem.get('detailed')
            self.genres[appt.get('value')] = genre_item

        for key, item in self.genres.items():
            genre = Genre(
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


def create_group():
    wiring = Wiring()
    default_group = Group(name='default', limit_per_day=10000)
    unlim_group = Group(name='unlim', limit_per_day=9999999)

    wiring.groups.create(default_group)
    wiring.groups.create(unlim_group)


def update_group():
    wiring = Wiring()
    unlim_group = Group(name='unlim', limit_per_day=9999999)
    wiring.groups.update(unlim_group)


def fix_stat():
    wiring = Wiring()
    cnt = 0
    stats = wiring.stat.collection.find({'resource': {"$regex": "/books/[a-z0-9]*/content$"}})
    for item in stats:
        resource = item['resource']
        id = str(item['_id'])
        find = re.findall(r'/books/([a-z0-9]*)/content$', resource)
        id_new = find[0]
        wiring.stat.collection.update_one({'_id': bson.ObjectId(id)}, {'$set': {'resource': id_new, 'action': 'bd'}})
        cnt+= 1
    print('Book download: ' + str(cnt))

    cnt = 0
    stats = wiring.stat.collection.find({'resource': {"$regex": "/books/[a-z0-9]*$"}})
    for item in stats:
        resource = item['resource']
        id = str(item['_id'])
        find = re.findall(r'/books/([a-z0-9]*)$', resource)
        id_new = find[0]
        wiring.stat.collection.update_one({'_id': bson.ObjectId(id)}, {'$set': {'resource': id_new, 'action': 'bv'}})
        cnt+= 1
    print('Book view: ' + str(cnt))

    cnt = 0
    stats = wiring.stat.collection.find({'resource': {"$regex": "/books/by_author/[a-z0-9]*$"}})
    for item in stats:
        resource = item['resource']
        id = str(item['_id'])
        find = re.findall(r'/books/by_author/([a-z0-9]*)$', resource)
        id_new = find[0]
        wiring.stat.collection.update_one({'_id': bson.ObjectId(id)}, {'$set': {'resource': id_new, 'action': 'av'}})
        cnt+= 1
    print('Author view: ' + str(cnt))

    cnt = 0
    stats = wiring.stat.collection.find({'resource': {"$regex": "/books/by_genre/[a-z0-9]*$"}})
    for item in stats:
        resource = item['resource']
        id = str(item['_id'])
        find = re.findall(r'/books/by_genre/([a-z0-9]*)$', resource)
        id_new = find[0]
        wiring.stat.collection.update_one({'_id': bson.ObjectId(id)}, {'$set': {'resource': id_new, 'action': 'gv'}})
        cnt+= 1
    print('Genres view: ' + str(cnt))

# fix_stat()
