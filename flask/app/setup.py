"""
Configure things here
"""
import json

import structlog
from flask import Flask

from app.database import setup_db, init_db
from app.errors import setup_errors
from app.logging import setup_logging
from app.views import add_views

# Importing models so that DB is initialized
from app.models import (
    obd,
    user,
)


def create_app() -> Flask:
    server = Flask(
        __name__,
        static_folder="./static/dist/static",
        template_folder="./static/dist",
    )
    setup_logging()
    setup_errors(server)
    add_views(server)
    setup_db(server)
    init_db(server)

    @server.after_request
    def log_access(response):
        data = "<not printable>"
        if response.headers.get("Content-Type") == "application/json":
            try:
                data = response.get_data().decode("utf-8")
            except UnicodeDecodeError:
                pass
        log_message = None
        try:
            log_message = json.loads(data)
        except json.JSONDecodeError:
            log_message = data
        structlog.get_logger("access").info(
            "RESPONSE",
            status=response.status_code,
            data=log_message
        )

        return response

    return server
