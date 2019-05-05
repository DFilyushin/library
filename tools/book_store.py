from zipfile import ZipFile, ZIP_DEFLATED
import os
import re
import uuid
from PIL import Image
from io import BytesIO
import base64


class BookStore(object):
    """
    Class for extract book information from archive file
    """
    def __init__(self, library_path: str, tmp: str, size):
        self.zip = dict()
        self.tmp_path = tmp
        self.books_path = library_path
        self.size = size
        self.regexps = [
            {'name': 'isbn', 'regxp': r'<isbn>(\S*)</isbn>'},
            {'name': 'year', 'regxp': r'<year>(\S*)</year>'},
            {'name': 'city', 'regxp': r'<city>([\s\S]*)</city>'},
            {'name': 'name', 'regxp': r'<book-name>([\s\S]*)</book-name>'},
            {'name': 'publisher', 'regxp': r'<publisher>([\s\S]*)</publisher>'}
        ]
        self.binary_regexps = [
            r'<binary\s+content-type=\"([^\"]+)\"\s+id=\"{}\"[^>]*>([.\s\S]*)</binary>',
            r'<binary\s+id=\"{}\"\s+content-type=\"([^\"]+)\">([^\"]*)</binary>'
        ]
        self.fb2_info_keys = ['coverType', 'cover', 'year', 'city', 'isbn', 'annotation', 'publisher', 'name', 'publisher']

    def check_item_exist(self, zip_file: str, item: str)->bool:
        """
        Check out file in archive
        :param zip_file:
        :param item:
        :return:
        """
        zip_path = os.path.join(self.books_path, zip_file)
        try:
            zip_obj = self.zip[zip_file]
        except KeyError:
            zip_obj = ZipFile(zip_path)
            self.zip[zip_file] = zip_obj
        return item in zip_obj.namelist()

    def _resize_image(self, image: bytes)->bytes:
        imgByteArr = BytesIO()
        obj_file = BytesIO(image)
        dt = Image.open(obj_file)
        dt.thumbnail(self.size, Image.ANTIALIAS)
        dt.save(imgByteArr, format='PNG')
        return (imgByteArr.getvalue(), dt.height, dt.width)

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
        fb_info = dict.fromkeys(self.fb2_info_keys, '')
        mem = self._extract_book_to_memory(bookid)
        code_page = 'utf-8'
        start_eol = mem.find(b'\x0D')
        if start_eol > 0:
            norm_line = mem[:start_eol].decode('IBM437')  # Default code page
            find_encoding = re.findall('encoding="(.*?)"', norm_line)
            code_page = find_encoding[0]
        book_xml = mem.decode(code_page)
        find = re.findall(r"<coverpage>\s*(.*?)\s*</coverpage>", book_xml)
        if find:
            image = re.findall('=\"(.*?)\"', find[0])
            image_file_with_tag = image[0]
            if image_file_with_tag[0] == '#':
                file_name = image_file_with_tag[1:]
                file_name = str(file_name).replace(r'.', r'\.')
                for item in self.binary_regexps:
                    find = re.findall(item.format(file_name), book_xml, re.IGNORECASE)
                    if find:
                        c_ctype = find[0][0]
                        c_norm_data = base64.b64decode(find[0][1])
                        c_resized_image = self._resize_image(c_norm_data)
                        if c_resized_image:
                            c_data2 = base64.b64encode(c_resized_image[0])
                            fb_info['coverType'] = c_ctype
                            fb_info['cover'] = c_data2.decode('ascii')
                            fb_info['coverHeight'] = c_resized_image[1]
                            fb_info['coverWidth'] = c_resized_image[2]
                            break

        find = re.findall(r'<annotation>([\s\S]*)</annotation>', book_xml)
        if find:
            annotation = str(find[0]).strip()
            fb_info['annotation'] = annotation

        regexp_descr = r'<publish-info>([.\s\S]*)<\/publish-info>'
        find = re.findall(regexp_descr, book_xml)
        if find:
            description = str(find[0]).strip()
            for item in self.regexps:
                find_value = re.findall(item['regxp'], description)
                if find_value:
                    fb_info[item['name']] = str(find_value[0]).strip()
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
            zip_obj = self.zip[zip_name]
        except KeyError:
            zip_obj = ZipFile(zip_path)
            self.zip[zip_name] = zip_obj
        return zip_obj.read(fb_item)

    def extract_books(self, booksid):
        """
        Extract books
        :param booksid: id of file in archive
        :return: Name of archive
        """
        zip_list = [self.extract_book(book) for book in booksid]
        tmp_file = str(uuid.uuid1())  # name of zip archive
        tmp_path = os.path.join(self.tmp_path, tmp_file)
        zip_obj = ZipFile(tmp_path, 'w', ZIP_DEFLATED)
        for item in zip_list:
            zip_obj.write(item, os.path.basename(item))
            zip_obj.close()
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
            zip_obj = self.zip[zip_name]
        except KeyError:
            zip_obj = ZipFile(zip_path)
            self.zip[zip_name] = zip_obj
        target_file = zip_obj.extract(fb_item, self.tmp_path)
        if zipped:
            zip_target_file = '{}.zip'.format(bookid)
            zip_full_path = os.path.join(self.tmp_path, zip_target_file)
            new_zip = ZipFile(zip_full_path, 'w', ZIP_DEFLATED)
            new_zip.write(target_file)
            new_zip.close()
            return zip_full_path
        else:
            return target_file
