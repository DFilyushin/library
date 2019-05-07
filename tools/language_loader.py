import os
import io
from wiring import Wiring
from storage.language import Language


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
