import socket
import subprocess
import os
from prepare_db import prepare_db
import pytest
from flaskapp import create_app
import coverage
import signal
import multiprocessing
from config import DevConfig


def pytest_sessionstart(session):
    """
    Called after the Session object has been created and
    before performing collection and entering the run test loop.
    """
    prepare_db()


@pytest.fixture(scope="session")
def app():
    app = create_app()
    # multiprocessing.set_start_method("spawn")
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
    # coverage.process_startup()
    server = subprocess.Popen(
        ['flask', 'run', '--port', str(flask_port)], env=env)
    # server = subprocess.Popen(
    #     ['python', '-m', 'flask', 'run', '--port', str(flask_port)], env=env)
    try:
        yield server
    finally:
        # server.terminate()
        server.send_signal(signal.SIGTERM)

# @pytest.fixture(scope="session", autouse=True)
# def live_server(flask_port):
#     env = os.environ.copy()
#     # coverage.process_startup()
#     server = multiprocessing.Process(target=create_app, args=(DevConfig,))
#     server.start()
#     # server = subprocess.Popen(
#     #     ['python', '-m', 'flask', 'run', '--port', str(flask_port)], env=env)
#     try:
#         yield server
#     finally:
#         # server.terminate()
#         server.join()


# @pytest.fixture
# def client(app):
#     return app.test_client()
