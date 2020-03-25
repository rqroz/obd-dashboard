"""
Database module

Initialization happens here as do configurations
so that we aren't super locked into using one particular
lib for db connection
"""
from flask import Flask, g
from flask_sqlalchemy import SQLAlchemy

from app.config.database import DBConfig


DATABASE = SQLAlchemy()


def get_db_uri():
    if DBConfig.SQLITE:
        return 'sqlite:///../db.sqlite3'

    return f'postgresql+psycopg2://{DBConfig.USER}:{DBConfig.PASS}@{DBConfig.HOST}:{DBConfig.PORT}/{DBConfig.NAME}'


def setup_db(app: Flask):
    app.config['SQLALCHEMY_DATABASE_URI'] = get_db_uri()
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    DATABASE.init_app(app)
    app.before_request(add_db_to_request_context)


def init_db(app: Flask):
    with app.app_context():
        DATABASE.create_all()


def add_db_to_request_context():
    g.db_session = DATABASE.session
