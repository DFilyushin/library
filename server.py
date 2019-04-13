import os.path
import flask
import flask_cors
from flask import request
from storage.genre import GenreNotFound
from wiring import Wiring


env = os.environ.get("APP_ENV", "dev")
print("Starting application in {} mode".format(env))


class HabrAppDemo(flask.Flask):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        flask_cors.CORS(self)

        self.wiring = Wiring(env)

        # genre api
        self.route("/api/v1/genres/all")(self.get_all_genres)

        # authors api
        self.route("/api/v1/author/by_full_name/<last_name>/<first_name>/<middle_name>")(self.get_author)
        self.route("/api/v1/authors/id/<id>")(self.get_author_by_id)
        self.route("/api/v1/authors/by_name/<last_name>")(self.get_authors)
        self.route("/api/v1/authors/start_with/<start_text_lastname>")(self.get_authors_startwith)

        # books api
        self.route('/api/v1/book/id/<id>')(self.get_book)
        self.route("/api/v1/books/by_author/<author_id>")(self.get_books_by_author)
        self.route('/api/v1/books/by_name/<name>')(self.get_book_by_name)
        self.route('/api/v1/books/by_genre/<name>')(self.get_book_by_genre)
        self.route('/api/v1/books/search')(self.get_book_by_search)

    def row2dict(self, row):
        d = {}
        #  for column in row.__table__.columns:
        for column in row.__dict__:
            d[column] = str(getattr(row, column))
        return d

    def dataset2dict(self, dataset):
        result = []
        for row in dataset:
            result.append(self.row2dict(row))
        return result

    def get_books_by_author(self, author_id):
        """Get books by author"""
        dataset = self.wiring.book_dao.get_by_author(author_id)
        data = self.dataset2dict(dataset)
        return flask.jsonify({'status': 'Ok', 'data': data})

    def get_all_genres(self):
        """
        Get all genres
        :return: list of genres
        """
        dataset = self.wiring.genre_dao.get_all()
        genres = [self.row2dict(row) for row in dataset]
        result = {
            'status': 'Ok',
            'data': genres
        }
        return flask.jsonify(result)

    def get_author_by_id(self, id):
        """
        Get author by uniq Id
        :param id: Id of author
        :return: author
        """
        try:
            dataset = self.wiring.author_dao.get_by_id(id)
        except Exception as err:
            return flask.jsonify({
                'status': 'No',
                'message': str(err)
            })
        return flask.jsonify(self.row2dict(dataset))

    def get_author(self, last_name, first_name, middle_name):
        """
        Get authors by full name
        :param last_name:
        :param first_name:
        :param middle_name:
        :return: author
        """
        dataset = self.wiring.author_dao.get_by_names(first_name, last_name, middle_name)
        return flask.jsonify(self.row2dict(dataset))

    def get_authors(self, last_name):
        """
        Get authors by last name
        :param last_name:
        :return: list of authors
        """
        dataset = self.wiring.author_dao.get_by_last_name(last_name)
        result = [self.row2dict(row) for row in dataset]
        return flask.jsonify(result)

    def get_authors_startwith(self, start_text_lastname):
        """
        Get authors last_name startwith start_text
        :param start_text_lastname
        :return:
        """
        limit = request.args.get('limit', 0, int)
        skip = request.args.get('skip', 0, int)
        dataset = self.wiring.author_dao.get_by_start(start_text_lastname, limit=limit, skipped=skip)
        result = [self.row2dict(row) for row in dataset]
        return flask.jsonify(result)

    def get_book(self, id):
        dataset = self.wiring.book_dao.get_by_id(id)
        if not dataset:
            return flask.jsonify({'status': 'No', 'message': 'Not found book by id'})
        result = {
            'status': 'Ok',
            'data': self.row2dict(dataset)
        }
        return flask.jsonify(result)

    def get_book_by_name(self, name):
        dataset = self.wiring.book_dao.get_by_name(name)
        result = [self.row2dict(row) for row in dataset]
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
        dataset = self.wiring.book_dao.search_book(name=f_name, lang=f_lang, series=f_series, keyword=f_keyword, genre=f_genre)
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


app = HabrAppDemo("library_librusec")
app.config.from_object("{}_settings".format(env))
