from waitress import serve
from useralerts.api import create_app
from config import Config


serve(create_app(), listen=f'*:{Config.ALERTS_PORT}')
