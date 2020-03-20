"""
Application-level constants.
"""

class Environments:
    PRODUCTION = 'production'
    LOCAL = 'local'


class Defaults:
    ENVIRONMENT = Environments.LOCAL
    LOG_LEVEL = 'DEBUG'

    class DB:
        HOST = 'localhost'
        PORT = '3306'
        NAME = 'dashboard_db'
        USER = 'test'
        PASS = 'test'
        SQLITE = True
