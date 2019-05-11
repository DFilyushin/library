import os
import json
from flask import Blueprint
from flask import request
from flask import current_app as app
from flask import abort
from flask import jsonify
from flask import send_file
from app_utils import row2dict, dataset2dict
from storage.stat import Stat

book_api = Blueprint('books', __name__, url_prefix='/api/v1/books')

simple_view = ['id', 'authors', 'city', 'genres', 'isbn', 'lang', 'name', 'pub_name', 'publisher', 'series', 'sernum', 'year']
full_view = ['id', 'authors', 'city', 'genres', 'isbn', 'lang', 'name', 'pub_name', 'publisher', 'series', 'sernum', 'year', 'annotation']


def stat_it(wiring, action: str, resource: str, username: str):
    ip = request.environ.get('REMOTE_ADDR', request.remote_addr)
    stat = Stat(ip=ip, resource=resource, action=action, login=username)
    wiring.stat.create(stat)


@book_api.route('/<bookid>/')
def get_book(bookid):
    """
    Get book by bookId
    :param bookid: Id of book
    :return:
    """
    dataset = app.wiring.book_ext_dao.get_by_id(bookid)
    if not dataset:
        return abort(404)
    stat_it(app.wiring, 'bv', bookid, '')
    book = row2dict(dataset, full_view)
    cover_name = '{}.jpg'.format(book['id'])
    cover_path = os.path.join(app.wiring.settings.IMAGE_DIR, cover_name)
    is_exists = os.path.exists(cover_path)
    book['cover'] = '/cover/' + cover_name if is_exists else ""
    json_data = json.dumps(book, ensure_ascii=False).encode('utf8')
    response = app.response_class(
        response=json_data,
        status=200,
        mimetype='application/json'
    )
    return response


@book_api.route('/<bookid>/content')
def download_book(bookid):
    """
    Get book content
    :param bookid: Id of book
    :return:
    """
    session = app.check_session()
    if not session:
        return abort(403)
    file_type = request.args.get('type', 'fb2', str)
    if file_type not in app.wiring.settings.FORMATS:
        abort(400)
    dataset = app.wiring.book_dao.get_by_id(bookid)
    if not dataset:
        return abort(404)
    output_file = '{}.{}'.format(dataset.filename, file_type)
    full_path_to_file = app.wiring.book_store.extract_book(int(dataset.filename), file_type == 'zip')
    if not full_path_to_file:
        return abort(404)
    stat_it(app.wiring, 'bd', bookid, session.login)
    return send_file(
        full_path_to_file,
        mimetype='application/octet-stream',
        attachment_filename=output_file,
        as_attachment=True)


@book_api.route('/<booksids>/package')
def download_books(booksids: str):
    """
    Download book package
    :param booksids: book list separated comma
    :return: send zip-file
    """
    # check session
    session = app.check_session()
    if not session:
        return abort(403)
    ids = booksids.split(',')
    books = []
    for item in ids:
        book = app.wiring.book_dao.get_by_id(item)
        if book:
            books.append(book.filename)
        else:
            ids.remove(item)
    if not books:
        abort(404)
    zip_file = app.wiring.book_store.extract_books(books)

    # add to statistic
    if zip_file:
        for item in ids:
            stat_it(app.wiring, 'bd', item, session.login)
        return send_file(zip_file,
                           mimetype='application/zip',
                           attachment_filename='books.zip',
                           as_attachment=True)


@book_api.route('/by_author/<author_id>')
def get_books_by_author(author_id):
    """
    Get books by author
    :param author_id:
    :return:
    """
    dataset = app.wiring.book_dao.get_by_author(author_id)
    data = dataset2dict(dataset, simple_view)
    if not data:
        return abort(404)
    json_data = json.dumps(data, ensure_ascii=False).encode('utf8')
    response = app.response_class(
        response=json_data,
        status=200,
        mimetype='application/json'
    )
    return response


@book_api.route('/by_name/<name>')
def get_book_by_name(name):
    """
    Find books by name
    :param name:
    :return:
    """
    dataset = app.wiring.book_dao.get_by_name(name)
    result = [row2dict(row) for row in dataset]
    if not result:
        return abort(404)
    json_data = json.dumps(result, ensure_ascii=False).encode('utf8')
    response = app.response_class(
        response=json_data,
        status=200,
        mimetype='application/json'
    )
    return response


@book_api.route('/by_genre/<name>')
def get_book_by_genre(name):
    """
    Get books by genre
    :param name: Name of genre
    :return:
    """
    dataset = app.wiring.book_dao.books_by_genres(name)
    result = [row2dict(row) for row in dataset]
    json_data = json.dumps(result, ensure_ascii=False).encode('utf8')
    response = app.response_class(
        response=json_data,
        status=200,
        mimetype='application/json'
    )
    return response


@book_api.route('/search/')
def get_book_by_search():
    """
    Search book by name, series, genre, keyword
    :return:
    """
    f_name = request.args.get('name', '')
    f_lang = request.args.get('lang', '')
    f_series = request.args.get('series', '')
    f_keyword = request.args.get('keyword', '')
    f_genre = request.args.get('genre', '')
    f_limit = request.args.get('limit', app.wiring.settings.DEFAULT_LIMITS, int)
    f_skip = request.args.get('skip', app.wiring.settings.DEFAULT_SKIP_RECORD, int)
    dataset = app.wiring.book_dao.search_book(
        name=f_name, lang=f_lang, series=f_series, keyword=f_keyword, genre=f_genre, skip=f_skip, limit=f_limit)
    result = [row2dict(row) for row in dataset]
    json_data = json.dumps(result, ensure_ascii=False).encode('utf8')
    response = app.response_class(
        response=json_data,
        status=200,
        mimetype='application/json'
    )
    return response


@book_api.route('/<booksid>/fb2info')
def get_fb2info(booksid: str):
    book = app.wiring.book_dao.get_by_id(booksid)
    if not book:
        abort(404)
    d = app.wiring.book_store.get_book_info(book.filename)
    json_data = json.dumps(d, ensure_ascii=False).encode('utf8')
    response = app.response_class(
        response=json_data,
        status=200,
        mimetype='application/json'
    )
    return response


@book_api.route('/popular')
def popular_books():
    limit = request.args.get('limit', app.wiring.settings.DEFAULT_LIMITS, int)
    books = app.wiring.book_dao.get_popular_books(limit)
    if not books:
        abort(404)
    result = [row2dict(row) for row in books]
    json_data = json.dumps(result, ensure_ascii=False).encode('utf8')
    response = app.response_class(
        response=json_data,
        status=200,
        mimetype='application/json'
    )
    return response
