"""
Simple config module
"""
import os

import app.constants as constants


class Config:
    LOG_LEVEL = os.getenv('LOG_LEVEL', constants.Defaults.LOG_LEVEL)
    ENVIRONMENT = os.getenv('ENVIRONMENT', constants.Defaults.ENVIRONMENT)
    DEBUG = ENVIRONMENT != constants.Environments.PRODUCTION
    BASE_URL = os.getenv('BASE_URL', 'http://localhost:5000')

    # DB Config
    class Database:
        HOST = os.getenv('DB_HOST', constants.Defaults.DB.HOST)
        PORT = os.getenv('DB_PORT', constants.Defaults.DB.PORT)
        NAME = os.getenv('DB_NAME', constants.Defaults.DB.NAME)
        USER = os.getenv('DB_USER', constants.Defaults.DB.USER)
        PASS = os.getenv('DB_PASS', constants.Defaults.DB.PASS)
