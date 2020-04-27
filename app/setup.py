"""
Configure things here
"""
import json
import locale

import structlog
from flask import Flask

from app.constants import Defaults
from app.database import setup_db, init_db
from app.errors import setup_errors
from app.logging import setup_logging
from app.plotly_dash.dashboard import init_plotly_dash
from app.views import add_views
from app.utils.encoders import DefaultJSONEncoder

# Importing models so that DB is initialized
from app.models import (
    obd,
    user,
)
from app.models.odb import (
    engine,
    fuel,
    gps,
    session,
)


def create_app() -> Flask:
    locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')
    server = Flask(
        __name__,
        static_folder=Defaults.FRONTEND_DIR,
        template_folder=Defaults.FRONTEND_DIR,
    )
    server.json_encoder = DefaultJSONEncoder
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

    init_plotly_dash(server)

    return server
