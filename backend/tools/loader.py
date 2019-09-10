from wiring import Wiring
from tools.book_loader import BookLoader
from tools.library_extractor import ZipArchiveProcessor
from tools.group_creator import create_group
from tools.update_version import update_version
from tools.language_loader import LanguageLoader
from tools.genre_loader import GenreLoader

# Import new data

# 1 step - import index files with books and authors
# 2 step - import from zips
# 3 step - import genres
# 4 step - import language
# 5 step - create groups
# Final - update library version


if __name__ == '__main__':
    wiring = Wiring()

    # 1
    index = BookLoader(wiring)
    index.process()

    # 2
    zip_loader = ZipArchiveProcessor(wiring)
    zip_loader.process()

    # 3
    genre_loader = GenreLoader(wiring)
    genre_loader.process()

    # 4
    lang_loader = LanguageLoader(wiring)
    lang_loader.process()

    # 5
    create_group(wiring)

    # Final - update version library
    update_version(wiring)
