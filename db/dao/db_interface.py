import psycopg
from psycopg.rows import dict_row
import aiosql
from functools import wraps
from datetime import datetime

queries = aiosql.from_path('db/sql', 'psycopg')


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

# ------------------------- USERS ---------------------------------------

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


# -------------------------- CITIES ---------------------------------------

# -------------------------- GET CITIES -----------------------------------


    @check_connection
    def get_all_cities(self) -> list[dict]:
        with psycopg.connect(self._connection_url, row_factory=dict_row) as conn:
            return [city for city in queries.get_all_cities(conn)]

    @check_connection
    def get_city_id(self, city_name: str):
        with psycopg.connect(self._connection_url) as conn:
            res = queries.get_city_id(conn, city_name=city_name)
            return res

# ------------------------ ADD CITIES -----------------------------------

    @check_connection
    def add_city(self, city_name: str) -> None:
        with psycopg.connect(self._connection_url) as conn:
            queries.add_city(conn, city_name=city_name)


# ----------------------- DELETE CITIES ---------------------------------

    @check_connection
    def delete_all_cities(self) -> None:
        with psycopg.connect(self._connection_url) as conn:
            queries.delete_all_cities(conn)

    @check_connection
    def delete_city_by_name(self, city_name: str) -> None:
        with psycopg.connect(self._connection_url) as conn:
            queries.delete_city_by_name(conn, city_name=city_name)

# ------------------------- ZIP CODES -----------------------------------

# ------------------------- GET ZIP CODES -------------------------------

    @check_connection
    def get_all_zip_codes(self) -> list[dict]:
        with psycopg.connect(self._connection_url, row_factory=dict_row) as conn:
            return [zip_code for zip_code in queries.get_all_zip_codes(conn)]

    @check_connection
    def get_city_id_by_zip_code(self, zip_code: int) -> int:
        with psycopg.connect(self._connection_url) as conn:
            return queries.get_city_id_by_zip_code(conn, zip_code=zip_code)

# ---------------------- ADD ZIP CODES ----------------------------------

    @check_connection
    def add_zip_code(self, zip_code: int, city_id: int) -> None:
        with psycopg.connect(self._connection_url) as conn:
            queries.add_zip_code(conn, zip_code=zip_code, city_id=city_id)

# --------------------- DELETE ZIP CODES ---------------------------------

    @check_connection
    def delete_all_zip_codes(self) -> None:
        with psycopg.connect(self._connection_url) as conn:
            queries.delete_all_zip_codes(conn)

    @check_connection
    def delete_zip_code(self, zip_code: int) -> None:
        with psycopg.connect(self._connection_url) as conn:
            queries.delete_zip_code(conn, zip_code=zip_code)


# --------------------- MAKES ------------------------------------

# --------------------- GET MAKES --------------------------------

    @check_connection
    def get_all_makes(self) -> list[dict]:
        with psycopg.connect(self._connection_url, row_factory=dict_row) as conn:
            return [make for make in queries.get_all_makes(conn)]

    @check_connection
    def get_make_info(self, make_name: str) -> dict:
        with psycopg.connect(self._connection_url, row_factory=dict_row) as conn:
            return queries.get_make_info(conn, make_name=make_name)

# --------------------- ADD MAKES ---------------------------------

    @check_connection
    def add_make(self, make_name: str) -> None:
        with psycopg.connect(self._connection_url) as conn:
            queries.add_make(conn, make_name=make_name)

# --------------------- DELETE MAKES ------------------------------

    @check_connection
    def delete_all_makes(self) -> None:
        with psycopg.connect(self._connection_url) as conn:
            queries.delete_all_makes(conn)

    @check_connection
    def delete_make_by_name(self, make_name: str) -> None:
        with psycopg.connect(self._connection_url) as conn:
            queries.delete_make_by_name(conn, make_name=make_name)


# -------------------- BODY STYLES -------------------------------

# -------------------- GET BODY STYLES ---------------------------


    @check_connection
    def get_all_body_styles(self) -> list[dict]:
        with psycopg.connect(self._connection_url, row_factory=dict_row) as conn:
            return [body_style for body_style in queries.get_all_body_styles(conn)]

    @check_connection
    def get_body_style_info(self, body_style_name: str) -> dict:
        with psycopg.connect(self._connection_url, row_factory=dict_row) as conn:
            return queries.get_body_style_info(conn, body_style_name=body_style_name)

# ------------------- ADD BODY STYLES ----------------------------

    @check_connection
    def add_body_style(self, body_style_name: str) -> None:
        with psycopg.connect(self._connection_url, row_factory=dict_row) as conn:
            queries.add_body_style(conn, body_style_name=body_style_name)

# ------------------ DELETE BODY STYLES --------------------------

    @check_connection
    def delete_all_body_styles(self) -> None:
        with psycopg.connect(self._connection_url, row_factory=dict_row) as conn:
            queries.delete_all_body_styles(conn)


# ------------------- WEBSITE BODY STYLES ---------------------------

# ------------------- WEB BODY STYLES GET ---------------------------

    @check_connection
    def get_all_website_body_styles(self) -> list[dict]:
        with psycopg.connect(self._connection_url, row_factory=dict_row) as conn:
            return [web_body_style for web_body_style in queries.get_all_website_body_styles(conn)]

    @check_connection
    def get_website_body_style_info(self, body_style_id: int) -> list[dict]:
        with psycopg.connect(self._connection_url, row_factory=dict_row) as conn:
            return [web_body_style for web_body_style in queries.get_website_body_style_info(conn, body_style_id=body_style_id)]

# ------------------ ADD WEB BODY STYLE ------------------------------

    @check_connection
    def add_website_body_style(self, body_style_id: int, website_name: str, website_body_name: str) -> None:
        with psycopg.connect(self._connection_url, row_factory=dict_row) as conn:
            queries.add_website_body_style(
                conn, body_style_id=body_style_id, website_name=website_name, website_body_name=website_body_name)

# ---------------- DELETE WEB BODY STYLE -----------------------------

    @check_connection
    def delete_all_website_body_styles(self) -> None:
        with psycopg.connect(self._connection_url, row_factory=dict_row) as conn:
            queries.delete_all_website_body_styles(conn)

    @check_connection
    def delete_specific_website_body_style(self, body_style_id: int) -> None:
        with psycopg.connect(self._connection_url, row_factory=dict_row) as conn:
            queries.delete_specific_website_body_style(
                conn, body_style_id=body_style_id)

# ----------------- CAR MODELS ----------------------------------------

# ----------------- GET CAR MODELS ------------------------------------

    @check_connection
    def get_all_models(self) -> list[dict]:
        with psycopg.connect(self._connection_url, row_factory=dict_row) as conn:
            return [model for model in queries.get_all_models(conn)]

    @check_connection
    def get_models_by_make_id(self, make_id: int) -> list[dict]:
        with psycopg.connect(self._connection_url, row_factory=dict_row) as conn:
            return [model for model in queries.get_model_by_make_id(conn, make_id=make_id)]

    @check_connection
    def get_model_by_make_name(self, make_name: str) -> list[dict]:
        with psycopg.connect(self._connection_url, row_factory=dict_row) as conn:
            return [model for model in queries.get_model_by_make_name(conn, make_name=make_name)]

    @check_connection
    def get_model_by_body_style_id(self, body_style_id: int) -> list[dict]:
        with psycopg.connect(self._connection_url, row_factory=dict_row) as conn:
            return [model for model in queries.get_model_by_body_style_id(conn, body_style_id=body_style_id)]

    @check_connection
    def get_model_by_body_style_name(self, body_style_name: str) -> list[dict]:
        with psycopg.connect(self._connection_url, row_factory=dict_row) as conn:
            return [model for model in queries.get_model_by_body_style_name(conn, body_style_name=body_style_name)]

# ---------------------------- ADD MODEL -------------------------------------

    @check_connection
    def add_model(self, model_name: str, make_id: int, body_style_id: int) -> None:
        with psycopg.connect(self._connection_url, row_factory=dict_row) as conn:
            queries.add_model(conn, model_name=model_name,
                              make_id=make_id, body_style_id=body_style_id)

# ---------------------------- DELETE MODELS -------------------------------

    @check_connection
    def delete_all_models(self) -> None:
        with psycopg.connect(self._connection_url, row_factory=dict_row) as conn:
            queries.delete_all_models(conn)

    @check_connection
    def delete_model_by_model_name(self, model_name: str) -> None:
        with psycopg.connect(self._connection_url, row_factory=dict_row) as conn:
            queries.delete_model_by_model_name(conn, model_name=model_name)


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
