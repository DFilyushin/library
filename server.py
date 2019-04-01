import os.path
import flask
import flask_cors

from storage.genre import GenreNotFound
from wiring import Wiring


env = os.environ.get("APP_ENV", "dev")
print("Starting application in {} mode".format(env))


class HabrAppDemo(flask.Flask):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        flask_cors.CORS(self)

        self.wiring = Wiring(env)

        self.route("/api/v1/genres/all")(self.get_all_genres)
        self.route("/api/v1/author/<last_name>/<first_name>/<middle_name>")(self.get_author)
        self.route("/api/v1/author/id/<id>")(self.get_author_by_id)

    def row2dict(self, row):
        d = {}
        #  for column in row.__table__.columns:
        for column in row.__dict__:
            d[column] = str(getattr(row, column))
        return d

    def get_all_genres(self):
        dataset = self.wiring.genre_dao.get_all()
        result = []
        for row in dataset:
            result.append(self.row2dict(row))
        return flask.jsonify(result)

    def get_author_by_id(self, id):
        dataset = self.wiring.author_dao.get_by_id(id)
        return flask.jsonify(self.row2dict(dataset))

    def get_author(self, last_name, first_name, middle_name):
        dataset = self.wiring.author_dao.get_by_names(first_name, last_name, middle_name)
        return flask.jsonify(self.row2dict(dataset))

    def card(self, card_id_or_slug):
        try:
            card = self.wiring.card_dao.get_by_slug(card_id_or_slug)
        except CardNotFound:
            try:
                card = self.wiring.card_dao.get_by_id(card_id_or_slug)
            except (CardNotFound, ValueError):
                return flask.abort(404)
        return flask.jsonify({
            k: v
            for k, v in card.__dict__.items()
            if v is not None
        })


app = HabrAppDemo("habr-app-demo")
app.config.from_object("{}_settings".format(env))
