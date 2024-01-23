from os import environ, path
from dotenv import load_dotenv

basedir = path.abspath(path.dirname(__file__))
load_dotenv(path.join(basedir, ".env"), override=True)

ZIP_ROW_COUNT = 33788
MODEL_ROW_COUNT = 1415


class Config:
    """Set Flask config variables."""
    FLASK_APP = environ.get("FLASK_APP")
    ALERTS_EMAIL = environ.get("ALERTS_EMAIL")
    ALERTS_EMAIL_PASSWORD = environ.get("ALERTS_EMAIL_PASSWORD")
    CURRENT_DB = environ.get("CURRENT_DB")
    POSTGRES_DATABASE_URI = environ.get(environ.get("CURRENT_DB") + "_URI")
    SMTP_RETRY_LIMIT = environ.get("SMTP_RETRY_LIMIT", 5)


class ProdConfig(Config):
    FLASK_ENV = "production"
    DEBUG = False
    TESTING = False
    LIVESERVER_PORT = 8943
    SECRET_KEY = environ.get("PROD_SECRET_KEY")


class DevConfig(Config):
    FLASK_ENV = "development"
    DEBUG = True
    TESTING = True
    SECRET_KEY = environ.get("DEV_SECRET_KEY")
