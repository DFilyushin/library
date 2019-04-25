import os.path
import functools
import flask
import flask_cors
from flask import request
from flask import send_from_directory
from storage.author import AuthorNotFound
from storage.language import LanguageNotFound
from storage.stat import Stat
from wiring import Wiring
from readlib import get_fb_content, get_archive_file

env = os.environ.get("FLASK_ENV", "dev")
print("Starting application in {} mode".format(env))


def reg_stat(method):
    @functools.wraps(method)
    def wrapper(self, *args, **kwargs):
        stat = Stat(ip=flask.request.remote_addr, resource=flask.request.path)
        self.wiring.stat.create(stat)
        return method(self, *args, **kwargs)
    return wrapper


class HabrAppDemo(flask.Flask):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        flask_cors.CORS(self)

        self.wiring = Wiring(env)

        self.route("/ci", methods=['POST'])(self.cintegra)
        self.route("/")(self.index)

        # library api
        self.route("/api/v1/info")(self.get_library_info)

        # genre api
        self.route("/api/v1/genres")(self.get_all_genres)

        # authors api
        self.route("/api/v1/authors/<id>")(self.get_author_by_id)
        self.route("/api/v1/authors/by_full_name/<last_name>/<first_name>/<middle_name>")(self.get_author)
        self.route("/api/v1/authors/by_name/<last_name>")(self.get_authors)
        self.route("/api/v1/authors/start_with/<start_text_lastname>")(self.get_authors_startwith)
        self.route("/api/v1/authors/<id>/genres")(self.get_author_genres)

        # books api
        self.route("/api/v1/books/<bookid>")(self.get_book)
        self.route("/api/v1/books/<bookid>/content")(self.get_book_content)
        self.route("/api/v1/books/by_author/<author_id>")(self.get_books_by_author)
        self.route("/api/v1/books/by_name/<name>")(self.get_book_by_name)
        self.route("/api/v1/books/by_genre/<name>")(self.get_book_by_genre)
        self.route("/api/v1/books/search")(self.get_book_by_search)
        self.route("/api/v1/books/<booksids>/package")(self.download_books)
        self.route("/api/v1/books/<booksids>/fb2info")(self.get_fb2info)

        # language api
        self.route("/api/v1/languages/<languageId>/books")(self.get_books_by_language)
        self.route("/api/v1/languages")(self.get_languages)
        self.route("/api/v1/languages/<languageId>")(self.get_language)

    @reg_stat
    def get_fb2info(self, booksids: str):
        ids = booksids.split(',')
        books = []
        for item in ids:
            book = self.wiring.book_dao.get_by_id(item)
            if book:
                d = self.wiring.book_store.get_book_info(book.filename)
                books.append(d)
        if not books:
            flask.abort(404)
        return flask.jsonify(books)

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
        return flask.send_file(zip_file, mimetype='application/zip',
                               attachment_filename='books.zip', as_attachment=True)

    @reg_stat
    def get_books_by_language(self, languageId):
        limit = request.args.get('limit', 100, int)
        skip = request.args.get('skip', 0, int)
        dataset = self.wiring.book_dao.books_by_language(languageId, limit=limit, skip=skip)
        result = [self.row2dict(row) for row in dataset]
        return flask.jsonify(result)

    @reg_stat
    def get_languages(self):
        languages = self.wiring.book_dao.get_languages_by_books()
        list_genres = [row['lang'] for row in languages]
        return flask.jsonify(list_genres)

        try:
            dataset = self.wiring.language_dao.get_all()
        except Exception as e:
            return flask.abort(400)
        result = [self.row2dict(row) for row in dataset]
        if not result:
            return flask.abort(404)
        return flask.jsonify(result)

    def get_language(self, languageId):
        try:
            dataset = self.wiring.language_dao.get_by_id(languageId)
        except LanguageNotFound:
            return flask.abort(404)
        except Exception as e:
            return flask.abort(400)
        return flask.jsonify(self.row2dict(dataset))

    def exp_dict(self, item):
        out = dict()
        for key, value in item.items():
            if type(value) == dict:
                out[key] = self.exp_dict(value)
            elif type(value) == int:
                out[key] = int(value)
            else:
                out[key] = str(value)
        return out

    def row2dict(self, row):
        d = dict()
        for column in row.__dict__:
            attr = getattr(row, column)
            if type(attr) == list:
                in_list = []
                for item in attr:
                    if type(item) == dict:
                        in_record = self.exp_dict(item)
                        in_list.append(in_record)
                    else:
                        in_list.append(str(item))

                d[column] = in_list
            elif type(attr) == dict:
                d[column] = dict()
                d[column] = self.exp_dict(attr)
            else:
                attr_item = getattr(row, column)
                if type(attr_item) == int:
                    d[column] = int(getattr(row, column))
                else:
                    d[column] = str(getattr(row, column))
        return d

    def index(self):
        return send_from_directory(r'./web/build/', 'index.html')

    def static_file(self, path, subpath):
        return send_from_directory(r'./web/build/', path+'/'+subpath)

    def cintegra(self):
        secret = request.headers.get('X-Hub-Signature', None)
        if not secret:
            return flask.abort(404)
        json = request.json
        print(json)
        return '', 200

    def dataset2dict(self, dataset):
        result = []
        for row in dataset:
            result.append(self.row2dict(row))
        return result

    @reg_stat
    def get_all_genres(self):
        """
        Get all genres
        :return: list of genres
        """
        dataset = self.wiring.genre_dao.get_all()
        genres = [self.row2dict(row) for row in dataset]
        if not genres:
            return flask.abort(404)
        return flask.jsonify(genres)

    @reg_stat
    def get_author_by_id(self, id):
        """
        Get author by uniq Id
        :param id: Id of author
        :return: author
        """
        try:
            dataset = self.wiring.author_dao.get_by_id(id)
        except AuthorNotFound:
            return flask.abort(404)
        except Exception as err:
            return flask.abort(400)
        return flask.jsonify(self.row2dict(dataset))

    @reg_stat
    def get_author(self, last_name, first_name, middle_name):
        """
        Get authors by full name
        :param last_name:
        :param first_name:
        :param middle_name:
        :return: author
        """
        try:
            dataset = self.wiring.author_dao.get_by_names(first_name, last_name, middle_name)
        except AuthorNotFound:
            return flask.abort(404)
        except Exception as e:
            return flask.abort(400)
        return flask.jsonify(self.row2dict(dataset))

    @reg_stat
    def get_authors(self, last_name):
        """
        Get authors by last name
        :param last_name:
        :return: list of authors
        """
        limit = request.args.get('limit', 100, int)
        skip = request.args.get('skip', 0, int)
        try:
            dataset = self.wiring.author_dao.get_by_last_name(last_name, limit, skip)
        except Exception as e:
            return flask.abort(400)
        result = [self.row2dict(row) for row in dataset]
        if not result:
            return flask.abort(404)
        return flask.jsonify(result)

    @reg_stat
    def get_authors_startwith(self, start_text_lastname):
        """
        Get authors last_name startwith start_text
        :param start_text_lastname
        :return:
        """
        limit = request.args.get('limit', 100, int)
        skip = request.args.get('skip', 0, int)
        dataset = self.wiring.author_dao.get_by_start(start_text_lastname, limit=limit, skip=skip)
        result = [self.row2dict(row) for row in dataset]
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
        return flask.jsonify(self.row2dict(dataset))

    @reg_stat
    def get_book_by_name(self, name):
        """
        Find books by name
        :param name:
        :return:
        """
        dataset = self.wiring.book_dao.get_by_name(name)
        result = [self.row2dict(row) for row in dataset]
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
        f_limit = request.args.get('limit', 100, int)
        f_skip = request.args.get('skip', 0, int)
        dataset = self.wiring.book_dao.search_book(
            name=f_name, lang=f_lang, series=f_series, keyword=f_keyword, genre=f_genre, skip=f_skip, limit=f_limit)
        result = [self.row2dict(row) for row in dataset]
        return flask.jsonify(result)

    @reg_stat
    def get_book_by_genre(self, name):
        """
        Get books by genre
        :param name: Name of genre
        :return:
        """
        dataset = self.wiring.book_dao.books_by_genres(name)
        result = [self.row2dict(row) for row in dataset]
        return flask.jsonify(result)

    @reg_stat
    def get_books_by_author(self, author_id):
        """
        Get books by author
        :param author_id:
        :return:
        """
        dataset = self.wiring.book_dao.get_by_author(author_id)
        data = self.dataset2dict(dataset)
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
        zip_file = get_archive_file(self.wiring.settings.LIB_ARCHIVE, int(dataset.filename))
        zip = os.path.join(self.wiring.settings.LIB_ARCHIVE, zip_file)
        unzipped = get_fb_content(zip, dataset.filename+'.fb2', self.wiring.settings.TMP_DIR)
        if not unzipped:
            return flask.abort(404)
        return flask.send_file(unzipped, mimetype='application/octet-stream', attachment_filename=dataset.filename+'.fb2', as_attachment=True)

    @reg_stat
    def get_library_info(self):
        """
        Get library info
        :return:
        """
        authors_count = self.wiring.author_dao.get_count_authors()
        books_count = self.wiring.book_dao.get_count_books()
        version = self.wiring.library_dao.get_version()
        letters = self.wiring.author_dao.letters_by_lastname()
        list_letters = list(dict.fromkeys([row['_id'].upper() for row in letters if ord(row['_id']) >= 65]))

        library_info = {
            "version": version.version,
            "last_update": version.added,
            "authorsCount": authors_count,
            "booksCount": books_count,
            "authorsLetters": list_letters,
            "seriesCount": 0
        }
        return flask.jsonify(library_info)

    def get_author_genres(self, id):
        genres = self.wiring.book_dao.get_genres_by_author(id)
        list_genres = [row['genres'] for row in genres]
        return flask.jsonify(list_genres)

app = HabrAppDemo("library_librusec", static_url_path='/static', static_folder='./web/build/static')
app.config.from_object("{}_settings".format(env))
