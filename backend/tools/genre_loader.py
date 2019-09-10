import os
import io
from datetime import datetime
from wiring import Wiring
from storage.genre import Genre
import xml.etree.ElementTree as ET


class GenreLoader(object):
    def __init__(self, wiring: Wiring):
        self.wiring = wiring
        self.genres = dict()
        self.path = os.path.join(self.wiring.settings.LIB_INDEXES, 'genres.xml')

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

    def get_xml_genres(self):
        try:
            root = ET.parse(self.path).getroot()
        except FileNotFoundError:
            print('File {} not found'.format(self.path))
            return None

        for record in root.getchildren():  # genre
            genre_item = dict()
            genre_item['name'] = record.get('value')
            genre_item['parent'] = ''
            genre_item['title'] = dict()
            genre_item['detailed'] = dict()
            for elem in record.getchildren():
                if elem.tag == 'subgenres':
                    self.get_subgenre(elem, genre_item['name'])
                elif elem.tag == 'root-descr':
                    lang = elem.get('lang')
                    lang_title = elem.get('genre-title')
                    genre_item['title'][lang] = lang_title
                    genre_item['detailed'][elem.get('lang')] = elem.get('detailed')
            self.genres[record.get('value')] = genre_item

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

    def process(self):
        print('{}: Import genres...'.format(datetime.now()))
        self.get_xml_genres()
        print('{}: Done'.format(datetime.now()))


if __name__ == '__main__':
    w = Wiring()
    genre_loader = GenreLoader(w)
    genre_loader.process()
