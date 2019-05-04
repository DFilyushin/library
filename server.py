import os.path
from datetime import datetime, timedelta
import re
import functools
import json
import flask_cors
from flask import request
from flask import send_from_directory
from flask import Flask
from flask import abort
from flask import jsonify
from flask import send_file
from flask import make_response
from storage.author import AuthorNotFound
from storage.language import LanguageNotFound
from storage.stat import Stat
from storage.user import User, UserExists, UserNotFound
from storage.session import Session, SessionNotFound
from storage.starred_book import StarredBook, StarExists
from wiring import Wiring
from app_utils import row2dict, dataset2dict
from app_utils import get_periods

SESSION_ID = 'X-User-Session-ID'


env = os.environ.get("FLASK_ENV", "dev")
print("Starting application in {} mode".format(env))


def reg_stat(method):
    """
    Add statistic for action
    :param method:
    :return:
    """
    @functools.wraps(method)
    def wrapper(self, *args, **kwargs):
        session_id = request.headers.get(SESSION_ID)
        login = ''
        if session_id:
            session = self.wiring.sessions.get_session(session_id)
            login = session.login
        stat = Stat(ip=request.remote_addr, resource=request.path, login=login)
        self.wiring.stat.create(stat)
        return method(self, *args, **kwargs)
    return wrapper


class LibraryApp(Flask):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        flask_cors.CORS(self)

        self.wiring = Wiring(env)
        self.formats = ['zip', 'fb2']

        # library api
        self.route("/api/v1/info")(self.get_library_info)
        self.route("/api/v1/stat")(self.get_statistic)

        # genre api
        self.route("/api/v1/genres")(self.get_all_genres)

        # authors api
        self.route("/api/v1/authors")(self.get_all_authors)
        self.route("/api/v1/authors/<authorid>")(self.get_author_by_id)
        self.route("/api/v1/authors/start_with/<start_text_fullname>")(self.get_authors_startwith)
        self.route("/api/v1/authors/<id>/genres")(self.get_author_genres)

        # books api
        self.route("/api/v1/books/<bookid>")(self.get_book)
        self.route("/api/v1/books/<bookid>/content")(self.download_book)
        self.route("/api/v1/books/<booksids>/package")(self.download_books)
        self.route("/api/v1/books/by_author/<author_id>")(self.get_books_by_author)
        self.route("/api/v1/books/by_name/<name>")(self.get_book_by_name)
        self.route("/api/v1/books/by_genre/<name>")(self.get_book_by_genre)
        self.route("/api/v1/books/search")(self.get_book_by_search)
        self.route("/api/v1/books/<booksid>/fb2info")(self.get_fb2info)

        # language api
        self.route("/api/v1/languages/<languageId>/books")(self.get_books_by_language)
        self.route("/api/v1/languages")(self.get_languages)
        self.route("/api/v1/languages/<languageId>")(self.get_language)

        # users api
        self.route("/api/v1/users", methods=['POST'])(self.create_user)
        self.route("/api/v1/auth", methods=['POST'])(self.auth)
        self.route("/api/v1/logout", methods=['POST'])(self.logout)
        self.route("/api/v1/users/<login>", methods=['GET', 'DELETE'])(self.user_ep)
        self.route("/api/v1/users/books/<bookid>/starred", methods=['PUT', 'DELETE'])(self.starred)

    @staticmethod
    def get_client_ip():
        return request.environ.get('REMOTE_ADDR', request.remote_addr)

    def stat_it(self, action: str, resource: str, username: str):
        ip = self.get_client_ip()
        stat = Stat(ip=ip, resource=resource, action=action, login=username)
        self.wiring.stat.create(stat)

    def check_session(self):
        """
        Check current session
        :return: session object
        """
        if not self.wiring.settings.USE_SESSIONS:
            session = self.wiring.sessions.create('develop', self.get_client_ip())
            return session
        session_id = request.headers.get(SESSION_ID, '', str)
        return self.wiring.sessions.get_session(session_id)

    def auth(self):
        login = request.args.get('login', default=None, type=str)
        password = request.args.get('password', default=None, type=str)
        try:
            user = self.wiring.users.get_by_login(login)
        except UserNotFound:
            abort(404)
        if user.password != password:
            abort(401)
        ip = self.get_client_ip()
        # create session
        session = self.wiring.sessions.create(login, ip)
        response = app.response_class(
            response=json.dumps({'session': session.session_id}),
            status=201,
            mimetype='application/json'
        )
        return response

    def logout(self):
        """
        Logout user session
        :return:
        """
        session_id = request.headers.get(SESSION_ID)
        try:
            self.wiring.sessions.close(session_id)
        except SessionNotFound:
            abort(404)
        response = app.response_class(
            response=json.dumps({'status': 'ok'}),
            status=201,
            mimetype='application/json'
        )
        return response

    def starred(self, bookid):
        """
        Starred and unstarred book for user
        User information getting from session variable SESSION-ID
        :param bookid:
        :return:
        """
        session_id = request.headers.get(SESSION_ID)
        if not session_id:
            abort(403)
        try:
            session = self.wiring.sessions.get_session(session_id)
        except SessionNotFound:
            abort(403)
        if request.method == 'PUT':
            star = StarredBook(login=session.login, book_id=bookid)
            try:
                self.wiring.stars.create(star)
            except StarExists:
                abort(400)
        elif request.method == 'DELETE':
            self.wiring.stars.delete_by_star_pair(session.login, bookid)
        response = app.response_class(
            response=json.dumps({'status': 'ok'}),
            status=201,
            mimetype='application/json'
        )
        return response

    def create_user(self):
        """
        Create user
        :return:
        """
        login = request.args.get('login', default=None, type=str)
        password = request.args.get('password', default=None, type=str)
        find = re.findall(r'^[a-zA-Z](_(?!(\.|_))|\.(?!(_|\.))|[a-zA-Z0-9]){6,18}[a-zA-Z0-9]$', login)
        if not find:
            abort(500)
        user = User(login=login, password=password)
        try:
            result = self.wiring.users.create(user)
        except UserExists:
            abort(400)
        resp = jsonify(success=True)
        resp.status_code = 201
        return resp

    def user_ep(self, login):
        session_id = request.headers.get(SESSION_ID)
        try:
            session = self.wiring.sessions.get_session(session_id)
        except SessionNotFound:
            abort(400)
        if session.login != login:
            abort(404)
        if request.method == 'GET':
            starred_books = []
            result = {
                'lastLogin': session.started,
                'downloadCount': self.wiring.stat.downloads_by_login(login),
                'starredBooks': starred_books
            }
        elif request.method == 'DELETE':
            if self.wiring.users.delete(login):
                return make_response('', 204)

    def get_statistic(self):
        json_data = self.wiring.cache_db.get_value('stat')
        if json_data:
            response = app.response_class(
                response=json_data,
                status=200,
                mimetype='application/json'
            )
            return response

        periods = get_periods()
        top_down_book_ids = self.wiring.stat.top_download_books(10)
        top_view_book_ids = self.wiring.stat.top_viewed_books(10)

        downloads = dict()
        views = dict()
        for item in periods:
            downloads[item['name']] = self.wiring.stat.count_download(item['start'], item['end'])
            views[item['name']] = self.wiring.stat.count_viewed(item['start'], item['end'])

        top_download_books = []
        top_viewed_books = []
        for item in top_down_book_ids:
            book = self.wiring.book_dao.get_by_id(item['book_id'])
            if book:
                top_download_books.append(row2dict(book))
        for item in top_view_book_ids:
            book = self.wiring.book_dao.get_by_id(item['book_id'])
            if book:
                top_viewed_books.append(row2dict(book))
        stats = {
            'users': 0,
            'downloads': downloads,
            'views': views,
            'topDownloadBooks': top_download_books,
            'topViewBooks': top_viewed_books
        }
        json_data = json.dumps(stats)
        self.wiring.cache_db.set_value('stat', json_data)
        response = app.response_class(
            response=json_data,
            status=200,
            mimetype='application/json'
        )
        return response

    def get_all_authors(self):
        """
        Get all authors sorted by last name
        :return:
        """
        limit = int(request.args.get('limit', self.wiring.settings.DEFAULT_LIMITS, int))
        skip = int(request.args.get('skip', self.wiring.settings.DEFAULT_SKIP_RECORD, int))
        dataset = self.wiring.author_dao.get_all(limit, skip)
        result = [row2dict(row) for row in dataset]
        if not result:
            return abort(404)
        return jsonify(result)

    def get_fb2info(self, booksid: str):
        book = self.wiring.book_dao.get_by_id(booksid)
        if not book:
            abort(404)
        d = self.wiring.book_store.get_book_info(book.filename)
        return jsonify(d)

    def download_books(self, booksids: str):
        """
        Download book package
        :param booksids: book list separated comma
        :return: send zip-file
        """
        # check session
        session = self.check_session()
        if not session:
            return abort(403)
        ids = booksids.split(',')
        books = []
        for item in ids:
            book = self.wiring.book_dao.get_by_id(item)
            if book:
                books.append(book.filename)
            else:
                ids.remove(item)
        if not books:
            abort(404)
        zip_file = self.wiring.book_store.extract_books(books)

        # add to statistic
        if zip_file:
            for item in ids:
                self.stat_it('db', item, session.login)
        return send_file(zip_file,
                               mimetype='application/zip',
                               attachment_filename='books.zip',
                               as_attachment=True)

    def get_books_by_language(self, languageId):
        limit = request.args.get('limit', self.wiring.settings.DEFAULT_LIMITS, int)
        skip = request.args.get('skip', self.wiring.settings.DEFAULT_SKIP_RECORD, int)
        dataset = self.wiring.book_dao.books_by_language(languageId, limit=limit, skip=skip)
        result = [row2dict(row) for row in dataset]
        return jsonify(result)

    def get_languages(self):
        """
        Get available languages
        :return:
        """
        languages = self.wiring.book_dao.get_languages_by_books()
        list_genres = [row['lang'] for row in languages]
        return jsonify(list_genres)

    def get_language(self, languageId):
        try:
            dataset = self.wiring.language_dao.get_by_id(languageId)
        except LanguageNotFound:
            return abort(404)
        except Exception as e:
            return abort(400)
        return jsonify(row2dict(dataset))

    def get_all_genres(self):
        """
        Get all genres
        :return: list of genres
        """
        json_data = self.wiring.cache_db.get_value('genres')
        if json_data:
            response = app.response_class(
                response=json_data,
                status=200,
                mimetype='application/json'
            )
            return response

        dataset = self.wiring.genre_dao.get_all()
        genres = [row2dict(row) for row in dataset]
        if not genres:
            return abort(404)
        json_data = json.dumps(genres)
        self.wiring.cache_db.set_value('genres', json_data)
        response = app.response_class(
            response=json_data,
            status=200,
            mimetype='application/json'
        )
        return response

    def get_author_by_id(self, authorid):
        """
        Get author by uniq Id
        :param authorid: Id of author
        :return: author
        """
        try:
            dataset = self.wiring.author_dao.get_by_id(authorid)
        except AuthorNotFound:
            return abort(404)
        except Exception as err:
            return abort(400)
        return jsonify(row2dict(dataset))

    def get_authors_startwith(self, start_text_fullname):
        """
        Get authors last_name startwith start_text
        :param start_text_fullname
        :return:
        """
        limit = request.args.get('limit', self.wiring.settings.DEFAULT_LIMITS, int)
        skip = request.args.get('skip', self.wiring.settings.DEFAULT_SKIP_RECORD, int)
        dataset = self.wiring.author_dao.get_by_start(start_text_fullname, limit=limit, skip=skip)
        result = [row2dict(row) for row in dataset]
        if not result:
            return abort(404)
        return jsonify(result)

    def get_book(self, bookid):
        """
        Get book by bookId
        :param bookid: Id of book
        :return:
        """
        dataset = self.wiring.book_dao.get_by_id(bookid)
        if not dataset:
            return abort(404)
        return jsonify(row2dict(dataset))

    def get_book_by_name(self, name):
        """
        Find books by name
        :param name:
        :return:
        """
        dataset = self.wiring.book_dao.get_by_name(name)
        result = [row2dict(row) for row in dataset]
        if not result:
            return abort(404)
        return jsonify(result)

    def get_book_by_search(self):
        """
        Search book by name, series, genre, keyword
        :return:
        """
        f_name = request.args.get('name', '')
        f_lang = request.args.get('lang', '')
        f_series = request.args.get('series', '')
        f_keyword = request.args.get('keyword', '')
        f_genre = request.args.get('genre', '')
        f_limit = request.args.get('limit', self.wiring.settings.DEFAULT_LIMITS, int)
        f_skip = request.args.get('skip', self.wiring.settings.DEFAULT_SKIP_RECORD, int)
        dataset = self.wiring.book_dao.search_book(
            name=f_name, lang=f_lang, series=f_series, keyword=f_keyword, genre=f_genre, skip=f_skip, limit=f_limit)
        result = [row2dict(row) for row in dataset]
        return jsonify(result)

    def get_book_by_genre(self, name):
        """
        Get books by genre
        :param name: Name of genre
        :return:
        """
        dataset = self.wiring.book_dao.books_by_genres(name)
        result = [row2dict(row) for row in dataset]
        return jsonify(result)

    def get_books_by_author(self, author_id):
        """
        Get books by author
        :param author_id:
        :return:
        """
        dataset = self.wiring.book_dao.get_by_author(author_id)
        data = dataset2dict(dataset)
        if not data:
            return abort(404)
        return jsonify(data)

    def download_book(self, bookid):
        """
        Get book content
        :param bookid: Id of book
        :return:
        """
        session = self.check_session()
        if not session:
            return abort(403)
        file_type = request.args.get('type', 'fb2', str)
        if file_type not in self.formats:
            abort(400)
        dataset = self.wiring.book_dao.get_by_id(bookid)
        if not dataset:
            return abort(404)
        output_file = '{}.{}'.format(dataset.filename, file_type)
        full_path_to_file = self.wiring.book_store.extract_book(int(dataset.filename), file_type == 'zip')
        if not full_path_to_file:
            return abort(404)
        self.stat_it('db', bookid, session.login)
        return send_file(
            full_path_to_file,
            mimetype='application/octet-stream',
            attachment_filename=output_file,
            as_attachment=True)

    def get_library_info(self):
        """
        Get library info
        :return:
        """
        json_data = self.wiring.cache_db.get_value('info')
        if json_data:
            response = app.response_class(
                response=json_data,
                status=200,
                mimetype='application/json'
            )
            return response
        authors_count = self.wiring.author_dao.get_count_authors()
        books_count = self.wiring.book_dao.get_count_books()
        version = self.wiring.library_dao.get_version()
        user_count = self.wiring.users.get_count_users()

        library_info = {
            "version": version.version,
            "authorsCount": authors_count,
            "booksCount": books_count,
            "usersCount": user_count
        }
        json_data = json.dumps(library_info)
        self.wiring.cache_db.set_value('info', json_data, 18000)  # one hour cache
        response = app.response_class(
            response=json_data,
            status=200,
            mimetype='application/json'
        )
        return response

    def get_author_genres(self, id):
        genres = self.wiring.book_dao.get_genres_by_author(id)
        list_genres = [row['genres'] for row in genres]
        return jsonify(list_genres)


app = LibraryApp("library_librusec")
app.config.from_object("{}_settings".format(env))
