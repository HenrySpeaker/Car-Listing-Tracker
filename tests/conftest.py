import socket
import subprocess
import os
from prepare_db import prepare_db
import pytest
from flaskapp import create_app
import signal
from db.dbi.db_interface import DBInterface
from config import DevConfig


def pytest_sessionstart(session):
    """
    Called after the Session object has been created and
    before performing collection and entering the run test loop.
    """
    db_uri = DevConfig.POSTGRES_DATABASE_URI
    dbi = DBInterface(db_uri)

    dbi.delete_all_models()
    dbi.delete_all_makes()
    dbi.delete_all_body_styles()
    prepare_db()


@pytest.fixture(scope="session")
def app():
    app = create_app()
    return app


@pytest.fixture(scope="session")
def flask_port():
    # Ask OS for a free port.
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(("", 0))
        addr = s.getsockname()
        port = addr[1]
        return port


@pytest.fixture(scope="session", autouse=True)
def live_server(flask_port):
    env = os.environ.copy()
    server = subprocess.Popen(
        ['flask', 'run', '--port', str(flask_port)], env=env)

    try:
        yield server
    finally:
        server.send_signal(signal.SIGTERM)
