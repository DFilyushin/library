import os
import io
from datetime import datetime
from wiring import Wiring
from storage.language import Language, LanguageExists


class LanguageLoader(object):
    """
    Fb2 language loader
    """

    def __init__(self, wiring: Wiring):
        self.wiring = wiring
        self.path = os.path.join(self.wiring.settings.LIB_INDEXES, 'language.txt')

    def process_file(self):
        try:
            with io.open(self.path, encoding='utf-8') as file:
                for line in file:
                    yield line
        except FileNotFoundError:
            print('File {} not found'.format(self.path))

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
            except LanguageExists:
                pass
            except Exception as E:
                print('Line {} is skipped cause error {}'.format(line, str(E)))

    def process(self):

        print('{}: Import languages ...'.format(datetime.now()))

        lines = self.process_file()
        self.process_line(lines)

        print('{}: Done'.format(datetime.now()))


if __name__ == '__main__':
    w = Wiring()
    lang_loader = LanguageLoader(w)
    lang_loader.process()
