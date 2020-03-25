from flask import Flask, g, jsonify
from structlog import get_logger

from app.config import Config
from app.constants import Defaults


logger = get_logger(__name__)


def create_error_response(data, status_code: int):
    resp = jsonify(data)
    resp.status_code = status_code
    return resp


def setup_errors(app: Flask):
    """
    Add some error views for handling of the
    usual errors in a nice way
    """
    if Config.ENVIRONMENT != Defaults.ENVIRONMENT:
        @app.errorhandler(Exception)
        def error_handler_exception(error):
            logger.error('uncaught exception', error=error)
            return create_error_response({'message': 'An unexpected error occurred'}, 500)

    @app.errorhandler(404)
    def error_handler_404(error):
        return create_error_response({'message': 'Not found'}, 404)

    @app.errorhandler(400)
    def error_handler_400(error):
        return create_error_response({'message': error}, 400)

    @app.errorhandler(401)
    def error_handler_401(error):
        return create_error_response({'message': 'Unauthorized'}, 401)

    @app.errorhandler(405)
    def error_handler_405(error):
        return create_error_response({'message': 'Method not allowed on resource uri'}, 405)

    @app.errorhandler(500)
    def error_handler_500(error):
        return create_error_response({'message': 'An unexpected error occurred'}, 500)
