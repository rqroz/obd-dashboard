"""
App Initializer
"""
from app.config import Config
from app.setup import create_app


server = create_app()
if __name__ == "__main__":
    server.run("0.0.0.0", port="5000", debug=Config.DEBUG)
