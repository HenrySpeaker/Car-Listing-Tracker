from waitress import serve
from flaskapp import create_app


serve(create_app(), listen='*:80')
