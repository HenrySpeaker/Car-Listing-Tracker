import psycopg
from psycopg.rows import dict_row
import aiosql
from functools import wraps

queries = aiosql.from_path('db/sql', 'psycopg')


def check_connection(fn):
    @wraps(fn)
    def inner(*args, **kwargs):
        """Checks if a valid connection has been supplied when initiating the DAO and runs the supplied function if it is valid."""
        if getattr(args[0], "_valid_connection", None):
            fn(*args, **kwargs)

    return inner


class DAO:

    def __init__(self, db_name: str = "", db_user: str = "", db_password: str = "") -> None:
        self._db_name = db_name
        self._db_user = db_user
        self._db_password = db_password
        self._connection_url = "dbname=" + self._db_name + " user=" + \
            self._db_user + " password=" + self._db_password
        self._valid_connection = False

        try:
            with psycopg.connect(self._connection_url) as conn:
                self._valid_connection = True
        except psycopg.ProgrammingError as e:
            print(f"An error occurred: {e}")

    @check_connection
    def get_all_users(self) -> None:
        with psycopg.connect(self._connection_url, row_factory=dict_row) as conn:
            res = queries.get_all_users(conn)
            return res

    @check_connection
    def add_user(self, user_info: dict = {}) -> int:
        with psycopg.connect(self._connection_url, row_factory=dict_row) as conn:
            res = queries.add_user(
                conn, username=user_info["username"], email=user_info["email"], password_hash=user_info["password_hash"], notification_frequency=user_info["notification_frequency"])
            return res

    @check_connection
    def delete_all_users(self) -> None:
        with psycopg.connect(self._connection_url, row_factory=dict_row) as conn:
            queries.delete_all_users(conn)
