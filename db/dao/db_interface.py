import psycopg
from psycopg.rows import dict_row
import aiosql
from functools import wraps
from datetime import datetime

queries = aiosql.from_path('db/sql/user_queries.sql', 'psycopg')


def check_connection(fn):
    @wraps(fn)
    def inner(*args, **kwargs):
        """Checks if a valid connection has been supplied when initiating the DAO and runs the supplied function if it is valid."""
        if getattr(args[0], "_valid_connection", None):
            return fn(*args, **kwargs)

    return inner


class DBInterface:

    def __init__(self, connection_url: str = "") -> None:
        self._connection_url = connection_url
        self._valid_connection = False

        try:
            with psycopg.connect(self._connection_url) as conn:
                self._valid_connection = True
        except psycopg.ProgrammingError as e:
            print(f"An error occurred: {e}")

# ------------------------- GET USERS -----------------------------------
    @check_connection
    def get_all_users(self) -> list:
        with psycopg.connect(self._connection_url, row_factory=dict_row) as conn:
            res = queries.get_all_users(conn)
            user_list = [user for user in res]
        return user_list

    @check_connection
    def get_user_by_username(self, username: str = "") -> dict:
        with psycopg.connect(self._connection_url, row_factory=dict_row) as conn:
            res = queries.get_user_by_username(conn, username=username)
            return res

    @check_connection
    def get_user_by_email(self, email: str = "") -> dict:
        with psycopg.connect(self._connection_url, row_factory=dict_row) as conn:
            res = queries.get_user_by_email(conn, email=email)
            return res


# ------------------------ ADD USERS ------------------------------------------

    @check_connection
    def add_user(self, user_info: dict = {}) -> int:
        with psycopg.connect(self._connection_url, row_factory=dict_row) as conn:
            res = queries.add_user(
                conn, username=user_info["username"], email=user_info["email"], password_hash=user_info["password_hash"], notification_frequency=user_info["notification_frequency"])
            return res


# ----------------------- UPDATE USERS ---------------------------------------

    @check_connection
    def update_username_by_email(self, email: str = "", new_username: str = "") -> None:
        with psycopg.connect(self._connection_url, row_factory=dict_row) as conn:
            queries.update_username_by_email(
                conn,  username=new_username, email=email)

    @check_connection
    def update_email_by_username(self, new_email: str = "", username: str = "") -> None:
        with psycopg.connect(self._connection_url, row_factory=dict_row) as conn:
            queries.update_email_by_username(
                conn,  username=username, email=new_email)

    @check_connection
    def update_password_hash_by_username(self, new_password_hash: str, username: str) -> None:
        with psycopg.connect(self._connection_url, row_factory=dict_row) as conn:
            queries.update_password_hash_by_username(
                conn, password_hash=new_password_hash, username=username)

    @check_connection
    def update_notification_frequency_by_username(self, new_notification_frequency: int, username: str) -> None:
        with psycopg.connect(self._connection_url, row_factory=dict_row) as conn:
            queries.update_notification_frequency_by_username(conn,
                                                              username=username, notification_frequency=new_notification_frequency)

    @check_connection
    def update_last_login_by_username(self, username: str, login_datetime: datetime) -> None:
        with psycopg.connect(self._connection_url, row_factory=dict_row) as conn:
            queries.update_login_time_by_username(
                conn, username=username, last_login=login_datetime)


# ----------------------- DELETE USERS ---------------------------------------


    @check_connection
    def delete_all_users(self) -> None:
        with psycopg.connect(self._connection_url) as conn:
            queries.delete_all_users(conn)
            # conn.commit()

    @check_connection
    def delete_user_by_username(self, username: str) -> None:
        with psycopg.connect(self._connection_url) as conn:
            queries.delete_user_by_username(conn, username=username)


def main():  # pragma: no cover
    dao = DBInterface("postgresql://postgres:password@localhost/Car-Listings")
    dao.delete_all_users()
    user_list = [{"username": f"username{i}", "email": f"user{i}@email.com",
                  "password_hash": f"password_hash{i}", "notification_frequency": 7} for i in range(1, 11)]
    for user in user_list:
        dao.add_user(user)

    print(dao.get_user_by_username("not a user"))


if __name__ == "__main__":
    main()  # pragma: no cover
