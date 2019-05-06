from flask import Blueprint
from flask import request
from flask import current_app as app
from flask import abort
from flask import jsonify
from flask import send_file
from app_utils import row2dict, dataset2dict

book_api = Blueprint('books', __name__, url_prefix='/api/v1/books')


@book_api.route('/<bookid>/')
def get_book(bookid):
    """
    Get book by bookId
    :param bookid: Id of book
    :return:
    """
    dataset = app.wiring.book_dao.get_by_id(bookid)
    if not dataset:
        return abort(404)
    return jsonify(row2dict(dataset))


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
    # self.stat_it('db', bookid, session.login)
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
        #for item in ids:
            # stat_it('db', item, session.login)
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
    data = dataset2dict(dataset)
    if not data:
        return abort(404)
    return jsonify(data)


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
    return jsonify(result)


@book_api.route('/by_genre/<name>')
def get_book_by_genre(name):
    """
    Get books by genre
    :param name: Name of genre
    :return:
    """
    dataset = app.wiring.book_dao.books_by_genres(name)
    result = [row2dict(row) for row in dataset]
    return jsonify(result)


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
    return jsonify(result)


@book_api.route('/<booksid>/fb2info')
def get_fb2info(booksid: str):
    book = app.wiring.book_dao.get_by_id(booksid)
    if not book:
        abort(404)
    d = app.wiring.book_store.get_book_info(book.filename)
    return jsonify(d)
