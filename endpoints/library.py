import json
from flask import Blueprint, abort, current_app as app
from app_utils import row2dict
from app_utils import get_periods


library_api = Blueprint('library', __name__, url_prefix='/api/v1')


@library_api.route('/info')
def get_library_info():
    """
    Get library info
    :return:
    """
    json_data = app.wiring.cache_db.get_value('info')
    if json_data:
        response = app.response_class(
            response=json_data,
            status=200,
            mimetype='application/json'
        )
        return response
    authors_count = app.wiring.author_dao.get_count_authors()
    books_count = app.wiring.book_dao.get_count_books()
    version = app.wiring.library_dao.get_version()
    user_count = app.wiring.users.get_count_users()

    library_info = {
        "version": version.version,
        "authorsCount": authors_count,
        "booksCount": books_count,
        "usersCount": user_count
    }
    json_data = json.dumps(library_info)
    app.wiring.cache_db.set_value('info', json_data, 18000)  # one hour cache
    response = app.response_class(
        response=json_data,
        status=200,
        mimetype='application/json'
    )
    return response


@library_api.route('/stat')
def get_statistic():
    json_data = app.wiring.cache_db.get_value('stat')
    if json_data:
        response = app.response_class(
            response=json_data,
            status=200,
            mimetype='application/json'
        )
        return response

    periods = get_periods()
    top_down_book_ids = app.wiring.stat.top_download_books(10)
    top_view_book_ids = app.wiring.stat.top_viewed_books(10)

    downloads = dict()
    views = dict()
    for item in periods:
        downloads[item['name']] = app.wiring.stat.count_download(item['start'], item['end'])
        views[item['name']] = app.wiring.stat.count_viewed(item['start'], item['end'])

    top_download_books = []
    top_viewed_books = []
    for item in top_down_book_ids:
        book = app.wiring.book_dao.get_by_id(item['book_id'])
        if book:
            top_download_books.append(row2dict(book))
    for item in top_view_book_ids:
        book = app.wiring.book_dao.get_by_id(item['book_id'])
        if book:
            top_viewed_books.append(row2dict(book))
    user_count = app.wiring.users.get_count_users()

    stats = {
        'users': user_count,
        'downloads': downloads,
        'views': views,
        'topDownloadBooks': top_download_books,
        'topViewBooks': top_viewed_books
    }
    json_data = json.dumps(stats)
    app.wiring.cache_db.set_value('stat', json_data)
    response = app.response_class(
        response=json_data,
        status=200,
        mimetype='application/json'
    )
    return response
