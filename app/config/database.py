"""
Database config
"""
import os
import app.constants as constants

# DB Config
class DBConfig:
    HOST = os.getenv('DB_HOST', constants.Defaults.DB.HOST)
    PORT = os.getenv('DB_PORT', constants.Defaults.DB.PORT)
    NAME = os.getenv('DB_NAME', constants.Defaults.DB.NAME)
    USER = os.getenv('DB_USER', constants.Defaults.DB.USER)
    PASS = os.getenv('DB_PASS', constants.Defaults.DB.PASS)
    SQLITE = (
        os.getenv('DB_SQLITE', '').upper() == 'TRUE'
        if os.getenv('DB_SQLITE')
        else constants.Defaults.DB.SQLITE
    )
