import os.path
import re
import functools
import json
import flask
import flask_cors
from flask import request
from flask import send_from_directory
from storage.author import AuthorNotFound
from storage.language import LanguageNotFound
from storage.stat import Stat
from storage.user import User, UserNotFound, UserExists
from wiring import Wiring
from readlib import get_fb_content, get_archive_file
from app_utils import row2dict, dataset2dict

env = os.environ.get("FLASK_ENV", "dev")
print("Starting application in {} mode".format(env))


def reg_stat(method):
    @functools.wraps(method)
    def wrapper(self, *args, **kwargs):
        stat = Stat(ip=flask.request.remote_addr, resource=flask.request.path)
        self.wiring.stat.create(stat)
        return method(self, *args, **kwargs)
    return wrapper


class LibraryApp(flask.Flask):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        flask_cors.CORS(self)

        self.wiring = Wiring(env)

        self.route("/", defaults={'path': 'index.html'})(self.index)
        self.route("/<path:path>")(self.index)
        self.route("/static/js/<path:path>")(self.static_files)

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
        self.route("/api/v1/books/<bookid>/content")(self.get_book_content)
        self.route("/api/v1/books/by_author/<author_id>")(self.get_books_by_author)
        self.route("/api/v1/books/by_name/<name>")(self.get_book_by_name)
        self.route("/api/v1/books/by_genre/<name>")(self.get_book_by_genre)
        self.route("/api/v1/books/search")(self.get_book_by_search)
        self.route("/api/v1/books/<booksids>/package")(self.download_books)
        self.route("/api/v1/books/<booksid>/fb2info")(self.get_fb2info)

        # language api
        self.route("/api/v1/languages/<languageId>/books")(self.get_books_by_language)
        self.route("/api/v1/languages")(self.get_languages)
        self.route("/api/v1/languages/<languageId>")(self.get_language)

        # users api
        self.route("/api/v1/users", methods=['POST'])(self.create_user)
        self.route("/api/v1/users/<login>/books/<bookid>/starred", methods=['PUT', 'DELETE'])(self.starred_book)
        self.route("/api/v1/users/<login>", methods=['GET', 'DELETE'])(self.check_user_exists)

    def index(self, path):
        return send_from_directory('web/build', path)

    def static_files(self, path):
        return send_from_directory('web/build/static/js', path)

    def create_user(self):
        login = request.args.get('login' ,default=None, type=str)
        password = request.args.get('password', default=None, type=str)
        find = re.findall(r'^[a-zA-Z](_(?!(\.|_))|\.(?!(_|\.))|[a-zA-Z0-9]){6,18}[a-zA-Z0-9]$', login)
        if not find:
            flask.abort(500)
        user = User(login=login, password=password)
        try:
            result = self.wiring.users.create(user)
        except UserExists:
            flask.abort(400)
        resp = flask.jsonify(success=True)
        resp.status_code = 201
        return resp

    def starred_book(self, login, bookid):
        pass

    def check_user_exists(self, login):
        pass

    def get_statistic(self):
        stats = dict()
        stats['users'] = 0
        stats['books'] = 0
        stats['rpd'] = 0
        return flask.jsonify(stats)

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
            return flask.abort(404)
        return flask.jsonify(result)

    @reg_stat
    def get_fb2info(self, booksid: str):
        book = self.wiring.book_dao.get_by_id(booksid)
        if not book:
            flask.abort(404)
        d = self.wiring.book_store.get_book_info(book.filename)
        return flask.jsonify(d)

    @reg_stat
    def download_books(self, booksids: str):
        ids = booksids.split(',')
        books = []
        for item in ids:
            book = self.wiring.book_dao.get_by_id(item)
            if book:
                books.append(book.filename)
        if not books:
            flask.abort(404)
        zip_file = self.wiring.book_store.extract_books(books)
        return flask.send_file(zip_file,
                               mimetype='application/zip',
                               attachment_filename='books.zip',
                               as_attachment=True)

    @reg_stat
    def get_books_by_language(self, languageId):
        limit = request.args.get('limit', self.wiring.settings.DEFAULT_LIMITS, int)
        skip = request.args.get('skip', self.wiring.settings.DEFAULT_SKIP_RECORD, int)
        dataset = self.wiring.book_dao.books_by_language(languageId, limit=limit, skip=skip)
        result = [row2dict(row) for row in dataset]
        return flask.jsonify(result)

    @reg_stat
    def get_languages(self):
        languages = self.wiring.book_dao.get_languages_by_books()
        list_genres = [row['lang'] for row in languages]
        return flask.jsonify(list_genres)

    def get_language(self, languageId):
        try:
            dataset = self.wiring.language_dao.get_by_id(languageId)
        except LanguageNotFound:
            return flask.abort(404)
        except Exception as e:
            return flask.abort(400)
        return flask.jsonify(row2dict(dataset))

    @reg_stat
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
            return flask.abort(404)
        json_data = json.dumps(genres)
        self.wiring.cache_db.set_value('genres', json_data)
        response = app.response_class(
            response=json_data,
            status=200,
            mimetype='application/json'
        )
        return response

    @reg_stat
    def get_author_by_id(self, authorid):
        """
        Get author by uniq Id
        :param authorid: Id of author
        :return: author
        """
        try:
            dataset = self.wiring.author_dao.get_by_id(authorid)
        except AuthorNotFound:
            return flask.abort(404)
        except Exception as err:
            return flask.abort(400)
        return flask.jsonify(row2dict(dataset))

    @reg_stat
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
            return flask.abort(404)
        return flask.jsonify(result)

    @reg_stat
    def get_book(self, bookid):
        """
        Get book by bookId
        :param bookid: Id of book
        :return:
        """
        dataset = self.wiring.book_dao.get_by_id(bookid)
        if not dataset:
            return flask.abort(404)
        return flask.jsonify(row2dict(dataset))

    @reg_stat
    def get_book_by_name(self, name):
        """
        Find books by name
        :param name:
        :return:
        """
        dataset = self.wiring.book_dao.get_by_name(name)
        result = [row2dict(row) for row in dataset]
        if not result:
            return flask.abort(404)
        return flask.jsonify(result)

    @reg_stat
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
        return flask.jsonify(result)

    @reg_stat
    def get_book_by_genre(self, name):
        """
        Get books by genre
        :param name: Name of genre
        :return:
        """
        dataset = self.wiring.book_dao.books_by_genres(name)
        result = [row2dict(row) for row in dataset]
        return flask.jsonify(result)

    @reg_stat
    def get_books_by_author(self, author_id):
        """
        Get books by author
        :param author_id:
        :return:
        """
        dataset = self.wiring.book_dao.get_by_author(author_id)
        data = dataset2dict(dataset)
        if not data:
            return flask.abort(404)
        return flask.jsonify(data)

    @reg_stat
    def get_book_content(self, bookid):
        """
        Get book content
        :param bookid: Id of book
        :return:
        """
        file_type = request.args.get('type', 'fb2')
        dataset = self.wiring.book_dao.get_by_id(bookid)
        if not dataset:
            return flask.abort(404)
        output_file = '{}.fb2'.format(dataset.filename)
        zip_file = self.wiring.book_store.extract_books([int(dataset.filename)])
        zip = os.path.join(self.wiring.settings.LIB_ARCHIVE, zip_file)
        unzipped = get_fb_content(zip, dataset.filename+'.fb2', self.wiring.settings.TMP_DIR)
        if not unzipped:
            return flask.abort(404)
        return flask.send_file(
            unzipped,
            mimetype='application/octet-stream',
            attachment_filename=output_file,
            as_attachment=True)

    @reg_stat
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
            "usersCount": user_count,
        }
        json_data = json.dumps(library_info)
        self.wiring.cache_db.set_value('info', json_data)
        response = app.response_class(
            response=json_data,
            status=200,
            mimetype='application/json'
        )
        return response

    def get_author_genres(self, id):
        genres = self.wiring.book_dao.get_genres_by_author(id)
        list_genres = [row['genres'] for row in genres]
        return flask.jsonify(list_genres)


app = LibraryApp("library_librusec")
app.config.from_object("{}_settings".format(env))
