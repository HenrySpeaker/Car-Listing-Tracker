from os import environ, path
from dotenv import load_dotenv

basedir = path.abspath(path.dirname(__file__))
load_dotenv(path.join(basedir, ".env"))

ZIP_ROW_COUNT = 33788
MODEL_ROW_COUNT = 1415


class Config:
    """Set Flask config variables."""
    FLASK_APP = environ.get("FLASK_APP")


class ProdConfig(Config):
    FLASK_ENV = "production"
    DEBUG = False
    TESTING = False
    POSTGRES_DATABASE_URI = environ.get("PROD_DATABASE_URI")
    LIVESERVER_PORT = 8943
    SECRET_KEY = environ.get("PROD_SECRET_KEY")


class DevConfig(Config):
    FLASK_ENV = "development"
    DEBUG = True
    TESTING = True
    POSTGRES_DATABASE_URI = environ.get("DEV_DATABASE_URI")
    SECRET_KEY = environ.get("DEV_SECRET_KEY")
