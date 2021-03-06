import os.path
import flask_cors
from flask import request
from flask import Flask
from wiring import Wiring


SESSION_ID = 'X-User-Session-ID'


class LibraryApp(Flask):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        flask_cors.CORS(self)
        self.wiring = Wiring(env)

    def check_session(self):
        """
        Check current session
        :return: session object
        """
        if not self.wiring.settings.USE_SESSIONS:
            client_ip = request.environ.get('REMOTE_ADDR', request.remote_addr)
            session = self.wiring.sessions.create('develop', client_ip)
            return session
        session_id = request.headers.get(SESSION_ID, '', str)
        return self.wiring.sessions.get_session(session_id)


env = os.environ.get("FLASK_ENV", "dev")
print("Starting application in {} mode".format(env))

app = LibraryApp("library_librusec")
app.config.from_object("{}_settings".format(env))
app.url_map.strict_slashes = False

from endpoints.genres import genres_api
from endpoints.library import library_api
from endpoints.authors import authors_api
from endpoints.books import book_api
from endpoints.users import users_api


app.register_blueprint(genres_api)
app.register_blueprint(library_api)
app.register_blueprint(authors_api)
app.register_blueprint(book_api)
app.register_blueprint(users_api)
