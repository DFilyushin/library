import json
from flask import Blueprint, abort, current_app as app
from app_utils import row2dict

GENRE_CACHE_EXPIRE = 604800  # the week
genres_api = Blueprint('genres', __name__, url_prefix='/api/v1/genres')


@genres_api.route('/')
def get_all_genres():
    """
    Get all genres
    :return: list of genres
    """
    json_data = app.wiring.cache_db.get_value('genres')
    if json_data:
        response = app.response_class(
            response=json_data,
            status=200,
            mimetype='application/json'
        )
        return response

    dataset = app.wiring.genre_dao.get_all()
    genres = [row2dict(row) for row in dataset]
    if not genres:
        return abort(404)
    json_data = json.dumps(genres, ensure_ascii=False).encode('utf8')
    app.wiring.cache_db.set_value('genres', json_data, GENRE_CACHE_EXPIRE)
    response = app.response_class(
        response=json_data,
        status=200,
        mimetype='application/json'
    )
    return response


