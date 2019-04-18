import os.path
import flask
import flask_cors
from flask import request
from storage.genre import GenreNotFound
from storage.author import AuthorNotFound
from wiring import Wiring


env = os.environ.get("FLASK_ENV", "dev")
print("Starting application in {} mode".format(env))


class HabrAppDemo(flask.Flask):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        flask_cors.CORS(self)

        self.wiring = Wiring(env)

        # library api
        self.route("/api/v1/info")(self.get_library_info)

        # genre api
        self.route("/api/v1/genres")(self.get_all_genres)

        # authors api
        self.route("/api/v1/authors/<id>")(self.get_author_by_id)
        self.route("/api/v1/authors/by_full_name/<last_name>/<first_name>/<middle_name>")(self.get_author)
        self.route("/api/v1/authors/by_name/<last_name>")(self.get_authors)
        self.route("/api/v1/authors/start_with/<start_text_lastname>")(self.get_authors_startwith)

        # books api
        self.route('/api/v1/books/<bookid>')(self.get_book)
        self.route('/api/v1/books/<bookid>/content')(self.get_book_content)
        self.route("/api/v1/books/by_author/<author_id>")(self.get_books_by_author)
        self.route('/api/v1/books/by_name/<name>')(self.get_book_by_name)
        self.route('/api/v1/books/by_genre/<name>')(self.get_book_by_genre)
        self.route('/api/v1/books/search')(self.get_book_by_search)

    def row2dict(self, row):
        d = {}
        for column in row.__dict__:
            attr = getattr(row, column)
            if type(attr) == list:
                in_list = []
                for item in attr:
                    in_record = {}
                    if type(item) == dict:
                        for key, value in item.items():
                            in_record[key] = str(value)
                        in_list.append(in_record)
                    else:
                        in_list.append(str(item))

                d[column] = in_list
            else:
                d[column] = str(getattr(row, column))
        return d

    def dataset2dict(self, dataset):
        result = []
        for row in dataset:
            result.append(self.row2dict(row))
        return result

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

    def get_book_by_genre(self, name):
        """
        Get books by genre
        :param name: Name of genre
        :return:
        """
        dataset = self.wiring.book_dao.books_by_genres(name)
        result = [self.row2dict(row) for row in dataset]
        return flask.jsonify(result)

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

    def get_book_content(self, bookid):
        """
        Get book content
        :param bookid: Id of book
        :return:
        """
        file_type = request.args.get('type', 'fb2')
        return 'Book {} of {}'.format(bookid, file_type)

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
            "authorsLetters": list_letters
        }
        return flask.jsonify(library_info)



app = HabrAppDemo("library_librusec")
app.config.from_object("{}_settings".format(env))
