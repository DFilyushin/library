import os
import zipfile
from wiring import Wiring
from tools.book_object import FBBookFile
from storage.book import Book, BookNotFound
from time import time


class ZipArchiveProcessor(object):

    def __init__(self, source: str, output_dir: str, size, wiring: Wiring):
        self.source = source
        self.output_dir = output_dir
        self.size = size
        self.wiring = wiring
        self.book_object = FBBookFile()

    @staticmethod
    def get_processed_files():
        processed = []
        try:
            with open('processed.txt', 'r') as file:
                for line in file:
                    processed.append(line.strip())
        except FileNotFoundError:
            pass
        return processed

    @staticmethod
    def set_processed_file(zip_name: str):
        with open('processed.txt', 'a+') as file:
            file.write(zip_name)
            file.write("\n")

    def get_zip_files(self):
        processed = self.get_processed_files()
        for file in filter(lambda x: x.endswith('.zip'), os.listdir(self.source)):
            if file in processed:
                print('Skipped file {} because already done.'.format(file))
                continue
            yield os.path.join(self.source, file)

    def get_archive_books(self, archive: str):
        zip = zipfile.ZipFile(archive)
        for book_file in zip.filelist:
            book = zip.read(book_file.filename)
            yield book_file.filename, book
        zip.close()
        self.set_processed_file(os.path.basename(archive))

    def process_archive_item(self, item):
        book_name, book_object = item
        book_num = book_name.split('.')[0]
        image_name = '{}.jpg'.format(book_num)
        output_file = os.path.join(self.output_dir, image_name)

        self.book_object.load_from_stream(book_object)

        if self.book_object.has_pub_info:
            try:
                book = self.wiring.book_dao.get_book_by_filename(book_num)
            except BookNotFound:
                return None

            book.isbn = self.book_object.isbn
            book.publisher = self.book_object.publisher
            book.year = self.book_object.year
            book.city = self.book_object.city
            book.pub_name = self.book_object.name
            book.annotation = self.book_object.annotation
            try:
                self.wiring.book_dao.update(book)
            except Exception as e:
                print('Update book {} error {}'.format(book_name, str(e)))

        if os.path.exists(output_file):
            return None
        mem = self.book_object.get_cover(self.size)
        if mem:
            with open(output_file, 'wb') as file:
                file.write(mem)

    def process(self):
        for file in self.get_zip_files():
            t0 = time()
            for item in self.get_archive_books(file):
                self.process_archive_item(item)
            print(file, time() - t0)


OUTPUT_DIR = r'e:\temp\images'
wiring = Wiring()
c = ZipArchiveProcessor(
    source=wiring.settings.LIB_ARCHIVE,
    output_dir=OUTPUT_DIR,
    size=wiring.settings.THUMBNAIL_SIZE,
    wiring=wiring)
c.process()