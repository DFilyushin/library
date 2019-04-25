from zipfile import ZipFile, ZIP_DEFLATED
import os
import re
import uuid


class BookStore(object):
    """
    Class for extract book information from archive file
    """
    def __init__(self, library_path: str, tmp: str):
        self.zip = dict()
        self.tmp_path = tmp
        self.books_path = library_path

    def check_item_exist(self, zip_file: str, item: str)->bool:
        zip_path = os.path.join(self.books_path, zip_file)
        try:
            zip = self.zip[zip_file]
        except KeyError:
            zip = ZipFile(zip_path)
            self.zip[zip_file] = zip
        result = item in zip.namelist()
        return result

    def get_zip_by_bookid(self, bookid: str)->str:
        """
        Find archive file by name of book file
        :param bookid:
        :return: Name of archive
        """
        book_num = int(bookid)
        gen_zip = (archive for archive in os.listdir(self.books_path) if archive.endswith('.zip') and 'lost' not in archive)
        gen_lost = (archive for archive in os.listdir(self.books_path) if archive.endswith('.zip') and 'lost' in archive)
        gens = [gen_zip, gen_lost]
        for gen in gens:
            for item in gen:
                fb, start, end = item[:-4].split('-')
                pos = end.find('_')
                if pos > -1:
                    end = end[:pos]
                start_num = int(start)
                end_num = int(end)
                if (book_num >= start_num) and (book_num <= end_num):
                    if self.check_item_exist(item, str(bookid)+'.fb2'):
                        return item

    def get_book_info(self, bookid: str)->dict:
        """
        Extract fb_info for book
        :param bookid: id of file in archive
        :return: dict {type: mimetype, data - string decoded in base64}
        """
        fb_info = {
            'coverType': '',
            'cover': '',
            'description': '',
            'year': '',
            'city': '',
            'isbn': '',
            'annotation': '',
            'publisher': '',
            'name': ''
        }
        mem = self._extract_book_to_memory(bookid)
        start_eol = mem.find(b'\x0D')
        norm_line = mem[:start_eol].decode('IBM437')  # Default code page
        code_page = re.findall('encoding="(.*?)"', norm_line)
        if not code_page:
            return None
        book_xml = mem.decode(code_page[0])
        find = re.findall(r"<coverpage>\s*(.*?)\s*</coverpage>", book_xml)
        if not find:
            return None
        image = re.findall('=\"(.*?)\"', find[0])
        image_file_with_tag = image[0]
        if image_file_with_tag[0] != '#':
            return fb_info
        image_file = image_file_with_tag[1:]
        r1 = image_file.split('.')
        regexp_cover = r'<binary\s+content-type=\"([^\"]+)\"\s+id=\"{}\.{}\"[^>]*>([.\s\S]*)</binary>'.format(r1[0], r1[1])
        find = re.findall( regexp_cover, book_xml, re.IGNORECASE)
        if find:
            fb_info['coverType'] = find[0][0]
            fb_info['cover'] = find[0][1]

        regexp_descr = r'<description>([.\s\S]*?)</description>'
        find = re.findall(regexp_descr, book_xml)
        if find:
            description = find[0]
            fb_info['description'] = description
            isbn = re.findall(r'<isbn>(\S*)</isbn>', description)
            if isbn:
                fb_info['isbn'] = isbn
            year = re.findall(r'<year>(\S*)</year>', description)
            if year:
                fb_info['year'] = year
            city = re.findall(r'<city>([\s\S]*)</city>', description)
            if city:
                fb_info['city'] = city
            annotation = re.findall('<annotation>([\s\S]*)</annotation>', description)
            if annotation:
                fb_info['annotation'] = annotation
            book_name = re.findall('<book-name>([\s\S]*)</book-name>', description)
            if book_name:
                fb_info['name'] = book_name
        return fb_info

    def _extract_book_to_memory(self, bookid: str)->bytes:
        """
        Extract archive book by bookid to array of bytes
        :param bookid: id of file in archive
        :return: array of bytes
        """
        fb_item = '{}.fb2'.format(bookid)
        zip_name = self.get_zip_by_bookid(bookid)
        zip_path = os.path.join(self.books_path, zip_name)
        if not zip_name:
            return None
        try:
            zip = self.zip[zip_name]
        except KeyError:
            zip = ZipFile(zip_path)
            self.zip[zip_name] = zip
        return zip.read(fb_item)

    def extract_books(self, booksid):
        """
        Extract books
        :param booksid: id of file in archive
        :return: Name of archive
        """
        zip_list = [self.extract_book(book) for book in booksid]
        tmp_file = str(uuid.uuid1())  # name of zip archive
        tmp_path = os.path.join(self.tmp_path, tmp_file)
        zip = ZipFile(tmp_path, 'w', ZIP_DEFLATED)
        for item in zip_list:
            zip.write(item, os.path.basename(item))
        zip.close()
        return tmp_path

    def extract_book(self, bookid: str, zipped: bool = False)->str:
        """
        Extract book from zip archive and save to tmp-path
        :param bookid: Code of book
        :param zipped: How return file?
        :return: Path to extracted file
        """
        fb_item = '{}.fb2'.format(bookid)
        zip_name = self.get_zip_by_bookid(bookid)
        zip_path = os.path.join(self.books_path, zip_name)
        if not zip_name:
            return ''
        try:
            zip = self.zip[zip_name]
        except KeyError:
            zip = ZipFile(zip_path)
            self.zip[zip_name] = zip
        target_file = zip.extract(fb_item, self.tmp_path)
        if zipped:
            zip_target_file = '{}.zip'.format(bookid)
            zip_full_path = os.path.join(self.tmp_path, zip_target_file)
            new_zip = ZipFile(zip_full_path, 'w', ZIP_DEFLATED)
            new_zip.write(target_file)
            new_zip.close()
            return zip_full_path
        else:
            return target_file
