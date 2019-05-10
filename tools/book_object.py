from io import BytesIO
import re
import base64
from PIL import Image, ImageFile

RE_BINARY = [
            r'<binary\s+content-type=\"([^\"]+)\"\s+id=\"{}\"[^>]*>([.\s\S]*)</binary>',
            r'<binary\s+id=\"{}\"\s+content-type=\"([^\"]+)\">([^\"]*)</binary>'
        ]
RE_PUBLISH_INFO = r'<publish-info>([.\s\S]*)<\/publish-info>'
RE_COVER = r"<coverpage>\s*(.*?)\s*</coverpage>"
RE_ANNOTATION = r'<annotation>([\s\S]*)</annotation>'
RE_ENCODING = r'encoding=[\'"](.*?)[\'"]'
RE_FIELDS = {
    'isbn': r'<isbn>(\S*)</isbn>',
    'year': r'<year>(\S*)</year>',
    'city': r'<city>([\s\S]*)</city>',
    'name': r'<book-name>([\s\S]*)</book-name>',
    'publisher': r'<publisher>([\s\S]*)</publisher>'}


class FBBookFile(object):
    """
    Fb book class
    for extract base fields about book, cover as png-image

    Mem_object is bytes of file in archive
    """
    def __init__(self):
        ImageFile.LOAD_TRUNCATED_IMAGES = True
        self.raw = None
        self.xml = None
        self.pub_info = None
        self.not_found_pub_info = False

    def load_from_stream(self, stream: bytes):
        self.raw = stream
        self.pub_info = None
        self.not_found_pub_info = False
        self.xml = None
        self._encode_raw_file()

    @staticmethod
    def _resize_image(image: bytes, th_size)->bytes:
        obj_file = BytesIO(image)
        try:
            dt = Image.open(obj_file).convert('RGB')
        except OSError:
            return None
        dt.thumbnail(th_size, Image.ANTIALIAS)
        output = BytesIO()
        dt.save(output, format='JPEG', quality=100, optimize=True, progressive=True)
        return output.getvalue()

    def _encode_pub_info(self):
        if not self.xml:
            return None
        if not self.pub_info:
            find = re.findall(RE_PUBLISH_INFO, self.xml)
            if find:
                self.pub_info = str(find[0]).strip()
            else:
                self.not_found_pub_info = True

    def _encode_raw_file(self):
        code_page = 'utf-8'
        start_eol = self.raw.find(b'\x0A')
        if start_eol > 0:
            norm_line = self.raw[:start_eol].decode('IBM437')  # Default code page
            find_encoding = re.findall(RE_ENCODING, norm_line)
            if find_encoding and find_encoding[0]:
                code_page = find_encoding[0]
        try:
            self.xml = self.raw.decode(code_page)
            return True
        except UnicodeDecodeError:
            return False

    def _extract_field(self, field):
        value = ''
        self._encode_pub_info()
        if self.pub_info:
            find_value = re.findall(RE_FIELDS[field], self.pub_info)
            if find_value:
                value = str(find_value[0]).strip()
        return value

    @property
    def annotation(self)->str:
        result = ''
        if not self.xml:
            return None
        find = re.findall(RE_ANNOTATION, self.xml)
        if find:
            result = str(find[0]).strip()
        return result

    @property
    def year(self)->str:
        return self._extract_field('year')

    @property
    def city(self)->str:
        return self._extract_field('city')

    @property
    def publisher(self)->str:
        return self._extract_field('publisher')

    @property
    def content(self)->str:
        if not self.xml:
            return None
        return self.xml

    @property
    def name(self)->str:
        return self._extract_field('name')

    @property
    def isbn(self)-> str:
        return self._extract_field('isbn')

    @property
    def has_pub_info(self)->bool:
        if self.not_found_pub_info:
            return False
        self._encode_pub_info()
        return not (self.pub_info is None)

    def get_cover(self, thumbnail_size:list)->bytes:
        if not self.xml:
            return None
        find = re.findall(RE_COVER, self.xml)
        if not find:
            return None
        if not find[0]:
            return None
        image = re.findall('=\"(.*?)\"', find[0])
        if not image:
            return None
        image_tagged = image[0]
        if image_tagged[0] != '#':
            return None
        inner_file_name = image_tagged[1:]
        inner_file_name = str(inner_file_name).replace(r'.', r'\.')
        for item in RE_BINARY:
            find = re.findall(item.format(inner_file_name), self.xml, re.IGNORECASE)
            if not find:
                continue
            try:
                c_norm_data = base64.b64decode(find[0][1])
            except:
                return None
            return self._resize_image(c_norm_data, thumbnail_size)


if __name__ == '__main__':
    image_size = (200, 200)
    book_file = FBBookFile()
    book_file.get_cover(image_size)
