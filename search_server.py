from waitress import serve
from datacollection.api import create_app
from config import Config


serve(create_app(), listen=f'*:{Config.SEARCH_PORT}')
