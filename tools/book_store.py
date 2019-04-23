from zipfile import ZipFile, ZIP_DEFLATED
import os
import re


class BookStore(object):
    """
    Class for extract book information from archive file
    """
    def __init__(self, library_path: str, tmp: str):
        self.zip = dict()
        self.tmp_path = tmp
        self.books_path = library_path

    def get_zip_by_bookid(self, bookid: str)->str:
        book_num = int(bookid)
        gen = (archive for archive in os.listdir(self.books_path) if archive.endswith('.zip') and not 'lost' in archive)
        for item in gen:
            fb, start, end = item[:-4].split('-')
            pos = end.find('_')
            if pos > -1:
                end = end[:pos]
            start_num = int(start)
            end_num = int(end)
            if (book_num >= start_num) and (book_num <= end_num):
                return item

    def get_book_cover(self, bookid: str)->dict:
        cover = dict()
        mem = self._extract_book_to_memory(bookid)
        start_eol = mem.find(b'\x0D')
        norm_line = mem[:start_eol].decode('IBM437')  # Default code page
        code_page = re.findall('encoding="(.*?)"', norm_line)
        if not code_page:
            return cover
        book_xml = mem.decode(code_page[0])
        find = re.findall(r"<coverpage>\s*(.*?)\s*</coverpage>", book_xml)
        if not find:
            return {}
        image = re.findall('=\"(.*?)\"', find[0])
        image_file_with_tag = image[0]
        if image_file_with_tag[0] != '#':
            return cover
        image_file = image_file_with_tag[1:]
        regexp_cover = r'<binary\s*id=\"{}\"\s*content-type=\"([\s\S]*)\">([.\s\S]*?)</binary>'.format(image_file)
        find = re.findall(regexp_cover, book_xml)
        if not find:
            return cover
        cover['type'] = find[0][0]
        cover['data'] = find[0][1]
        return cover

    def get_book_ext_info(self, bookid: str)->str:
        pass

    def _extract_book_to_memory(self, bookid: str)->bytes:
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

    def extract_book(self, bookid: str, zipped: bool = False)->str:
        """
        Extract book from zip archive and save to tmp-path
        :param bookid: Code of book
        :param zipped: How return file?
        :return:
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
