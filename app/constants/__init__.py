"""
Application-level constants.
"""

class Environments:
    PRODUCTION = 'production'
    LOCAL = 'local'


class Defaults:
    SECRET_KEY = 'my-secret-key'
    ENVIRONMENT = Environments.LOCAL
    LOG_LEVEL = 'DEBUG'
    FRONTEND_DIR = './static/dist/'

    class DB:
        HOST = 'localhost'
        PORT = '5432'
        NAME = 'dashboard_db'
        USER = 'test'
        PASS = 'test'
        SQLITE = True
