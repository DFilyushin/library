import json
from flask import request
from flask import jsonify
from flask import abort
from flask import Blueprint
from flask import current_app as app
from app_utils import row2dict
from storage.author import AuthorNotFound


authors_api = Blueprint('authors', __name__, url_prefix='/api/v1/authors')


@authors_api.route('/')
def get_all_authors():
    """
    Get all authors sorted by last name
    :return:
    """
    limit = int(request.args.get('limit', app.wiring.settings.DEFAULT_LIMITS, int))
    skip = int(request.args.get('skip', app.wiring.settings.DEFAULT_SKIP_RECORD, int))
    dataset = app.wiring.author_dao.get_all(limit, skip)
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


@authors_api.route('/<authorid>')
def get_author_by_id(authorid):
    """
    Get author by uniq Id
    :param authorid: Id of author
    :return: author
    """
    try:
        dataset = app.wiring.author_dao.get_by_id(authorid)
    except AuthorNotFound:
        return abort(404)
    except Exception as err:
        return abort(400)
    json_data = json.dumps(row2dict(dataset), ensure_ascii=False).encode('utf8')
    response = app.response_class(
        response=json_data,
        status=200,
        mimetype='application/json'
    )
    return response



@authors_api.route('/start_with/<start_text_fullname>')
def get_authors_startwith(start_text_fullname):
    """
    Get authors last_name startwith start_text
    :param start_text_fullname
    :return:
    """
    limit = request.args.get('limit', app.wiring.settings.DEFAULT_LIMITS, int)
    skip = request.args.get('skip', app.wiring.settings.DEFAULT_SKIP_RECORD, int)
    dataset = app.wiring.author_dao.get_by_start(start_text_fullname, limit=limit, skip=skip)
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


@authors_api.route('/<id>/genres')
def get_author_genres(id):
    genres = app.wiring.book_dao.get_genres_by_author(id)
    list_genres = [row['genres'] for row in genres]
    json_data = json.dumps(list_genres, ensure_ascii=False).encode('utf8')
    response = app.response_class(
        response=json_data,
        status=200,
        mimetype='application/json'
    )
    return response
