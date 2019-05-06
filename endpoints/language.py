from flask import Blueprint
from flask import abort
from flask import request
from flask import jsonify
from flask import current_app as app
from app_utils import row2dict
from storage.language import LanguageNotFound

language_api = Blueprint('language', __name__, url_prefix='/api/v1/languages')


@language_api.route('/<languageId>/books')
def get_books_by_language(languageId):
    limit = request.args.get('limit', app.wiring.settings.DEFAULT_LIMITS, int)
    skip = request.args.get('skip', app.wiring.settings.DEFAULT_SKIP_RECORD, int)
    dataset = app.wiring.book_dao.books_by_language(languageId, limit=limit, skip=skip)
    result = [row2dict(row) for row in dataset]
    return jsonify(result)


@language_api.route('/')
def get_languages():
    """
    Get available languages
    :return:
    """
    languages = app.wiring.book_dao.get_languages_by_books()
    list_genres = [row['lang'] for row in languages]
    return jsonify(list_genres)


@language_api.route('/<languageId>/')
def get_language(languageId):
    try:
        dataset = app.wiring.language_dao.get_by_id(languageId)
    except LanguageNotFound:
        return abort(404)
    except Exception as e:
        return abort(400)
    return jsonify(row2dict(dataset))
