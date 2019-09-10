from collections import OrderedDict
import json
from app_utils import row2dict
from wiring import Wiring
from app_const import CACHE_FOUR_WEEK

# Cache reload by deploy


def reload_stat(wiring: Wiring):

    # Reload cache for stat

    authors_count = wiring.author_dao.get_count_authors()
    books_count = wiring.book_dao.get_count_books()
    version = wiring.library_dao.get_version()

    library_info = {
        "version": version.version,
        "authorsCount": authors_count,
        "booksCount": books_count
    }
    json_data = json.dumps(library_info)
    wiring.cache_db.set_value('info', json_data, CACHE_FOUR_WEEK)  # four week cache


def reload_genre(wiring: Wiring):

    # Reload cache for genre

    dataset = wiring.genre_dao.get_all()
    genres = [row2dict(row) for row in dataset]
    if not genres:
        return None
    json_data = json.dumps(genres, ensure_ascii=False).encode('utf8')
    wiring.cache_db.set_value('genres', json_data, CACHE_FOUR_WEEK)


if __name__ == '__main__':
    w = Wiring()
    reload_genre(w)
    reload_stat(w)
