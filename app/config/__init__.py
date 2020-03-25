"""
Application-level constants
"""
import os

import app.constants as constants


class Config:
    LOG_LEVEL = os.getenv('LOG_LEVEL', constants.Defaults.LOG_LEVEL)
    ENVIRONMENT = os.getenv('ENVIRONMENT', constants.Defaults.ENVIRONMENT)
    DEBUG = ENVIRONMENT != constants.Environments.PRODUCTION
    BASE_URL = os.getenv('BASE_URL', 'http://localhost:5000')
