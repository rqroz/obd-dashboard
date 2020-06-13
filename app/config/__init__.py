"""
Application-level constants
"""
import os

import app.constants as constants


class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', constants.Defaults.SECRET_KEY)
    AUTH_TOKEN_NAME = os.getenv('AUTH_TOKEN_NAME_NAME', 'obd-auth-token')
    LOG_LEVEL = os.getenv('LOG_LEVEL', constants.Defaults.LOG_LEVEL)
    ENVIRONMENT = os.getenv('ENVIRONMENT', constants.Defaults.ENVIRONMENT)
    DEBUG = ENVIRONMENT != constants.Environments.PRODUCTION
    BASE_URL = os.getenv('BASE_URL', 'http://localhost:5000')
