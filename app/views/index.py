"""
App initializer
"""
import os
import requests

from flask import render_template
from app.config import Config
from app.constants import Environments


class IndexViews:
    @classmethod
    def add_views(cls, server):
        server.add_url_rule("/", defaults={'path': ''}, view_func=cls.index_view)
        server.add_url_rule("/<path:path>", view_func=cls.index_view)

    def index_view(path):
        if Config.ENVIRONMENT == Environments.LOCAL:
            return requests.get(f'http://localhost:8080/{path}').text
        return render_template("index.html")
