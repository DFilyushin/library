import re
import json
from flask import Blueprint
from flask import current_app as app
from flask import request
from flask import abort
from flask import jsonify
from flask import make_response
from storage.user import User, UserExists, UserNotFound
from storage.session import SessionNotFound
from storage.starred_book import StarredBook, StarExists

SESSION_ID = 'X-User-Session-ID'

users_api = Blueprint('users', __name__, url_prefix='/api/v1/users')


@users_api.route('/', methods=['POST'])
def create_user():
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
        result = app.wiring.users.create(user)
    except UserExists:
        abort(400)
    resp = jsonify(success=True)
    resp.status_code = 201
    return resp


@users_api.route('/auth', methods=['POST'])
def auth():
    login = request.args.get('login', default=None, type=str)
    password = request.args.get('password', default=None, type=str)
    try:
        user = app.wiring.users.get_by_login(login)
    except UserNotFound:
        abort(404)
    if user.password != password:
        abort(401)
    ip = app.get_client_ip()
    # create session
    session = app.wiring.sessions.create(login, ip)
    response = app.response_class(
        response=json.dumps({'session': session.session_id}),
        status=201,
        mimetype='application/json'
    )
    return response


@users_api.route('/logout', methods=['POST'])
def logout():
    """
    Logout user session
    :return:
    """
    session_id = request.headers.get(SESSION_ID)
    try:
        app.wiring.sessions.close(session_id)
    except SessionNotFound:
        abort(404)
    response = app.response_class(
        response=json.dumps({'status': 'ok'}),
        status=201,
        mimetype='application/json'
    )
    return response


@users_api.route('/<login>/', methods=['GET', 'DELETE'])
def user_ep(login):
    session_id = request.headers.get(SESSION_ID)
    try:
        session = app.wiring.sessions.get_session(session_id)
    except SessionNotFound:
        abort(400)
    if session.login != login:
        abort(404)
    if request.method == 'GET':
        starred_books = []
        result = {
            'lastLogin': session.started,
            'downloadCount': app.wiring.stat.downloads_by_login(login),
            'starredBooks': starred_books
        }
    elif request.method == 'DELETE':
        if app.wiring.users.delete(login):
            return make_response('', 204)


@users_api.route('/books/<bookid>/starred', methods=['PUT', 'DELETE'])
def starred(bookid):
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
        session = app.wiring.sessions.get_session(session_id)
    except SessionNotFound:
        abort(403)
    if request.method == 'PUT':
        star = StarredBook(login=session.login, book_id=bookid)
        try:
            app.wiring.stars.create(star)
        except StarExists:
            abort(400)
    elif request.method == 'DELETE':
        app.wiring.stars.delete_by_star_pair(session.login, bookid)
    response = app.response_class(
        response=json.dumps({'status': 'ok'}),
        status=201,
        mimetype='application/json'
    )
    return response
