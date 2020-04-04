"""
Index Views
"""
import os
import requests

from flask import render_template
from app.config import Config
from app.constants import Environments


class IndexViews:
    @classmethod
    def add_views(cls, server):
        server.add_url_rule('/', view_func=cls.index_view, methods=("GET",))

    def index_view():
        if Config.ENVIRONMENT == Environments.LOCAL:
            return requests.get('http://localhost:8080').text
        return render_template("index.html")
