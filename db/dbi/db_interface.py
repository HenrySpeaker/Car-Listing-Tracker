import psycopg
from psycopg.rows import dict_row
from psycopg import sql
import aiosql
from functools import wraps
from datetime import datetime
from db.body_styles import body_styles
from datetime import datetime

queries = aiosql.from_path('db/sql', 'psycopg')


def check_connection(fn):
    @wraps(fn)
    def inner(*args, **kwargs):
        """Checks if a valid connection has been supplied when initiating the DAO and runs the supplied function if it is valid."""
        if getattr(args[0], "_valid_connection", None) and args[0]._valid_connection:
            return fn(*args, **kwargs)
        else:
            raise RuntimeError("The database connection is not valid.")

    return inner


class DBInterface:

    def __init__(self, connection_url: str = "") -> None:
        self._connection_url = connection_url
        self._valid_connection = False

        try:
            with psycopg.connect(self._connection_url) as conn:
                self._valid_connection = True
        except (psycopg.ProgrammingError, psycopg.OperationalError) as e:
            print(f"An error occurred: {e}")

        if self._valid_connection:  # pragma: no cover
            # check to see if body_styles have been added to the table already
            with psycopg.connect(self._connection_url, row_factory=dict_row) as conn:
                curr_body_styles = self.get_all_body_styles()
                if not curr_body_styles:
                    for body_style in body_styles:
                        self.add_body_style(body_style_name=body_style)


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

    @check_connection
    def get_user_by_id(self, id: int) -> dict:
        with psycopg.connect(self._connection_url, row_factory=dict_row) as conn:
            res = queries.get_user_by_id(conn, id=id)
            return res


# ------------------------ ADD USERS ------------------------------------------


    @check_connection
    def add_user(self, user_info: dict = {}) -> int:
        with psycopg.connect(self._connection_url, row_factory=dict_row) as conn:
            queries.add_user(
                conn, username=user_info["username"], email=user_info["email"], password_hash=user_info["password_hash"], notification_frequency=user_info["notification_frequency"])


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

    @check_connection
    def update_last_alerted_by_id(self, id: int, last_alerted: datetime) -> None:
        with psycopg.connect(self._connection_url, row_factory=dict_row) as conn:
            queries.update_last_alerted_by_id(
                conn, id=id, last_alerted=last_alerted)


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
    def add_city(self, city_name: str, state_id: int) -> None:  # pragma: no cover
        with psycopg.connect(self._connection_url) as conn:
            queries.add_city(conn, city_name=city_name, state_id=state_id)


# ----------------------- DELETE CITIES ---------------------------------


    @check_connection
    def delete_all_cities(self) -> None:  # pragma: no cover
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
    def get_zip_code_info(self, zip_code: int) -> dict:
        with psycopg.connect(self._connection_url, row_factory=dict_row) as conn:
            return queries.get_zip_code_info(conn, zip_code=zip_code)

    @check_connection
    def get_zip_code_count(self) -> int:
        with psycopg.connect(self._connection_url) as conn:
            return queries.get_zip_code_count(conn)

    @check_connection
    def get_zip_code_by_id(self, zip_code_id: int) -> dict:
        with psycopg.connect(self._connection_url, row_factory=dict_row) as conn:
            return queries.get_zip_code_by_id(conn, zip_code_id=zip_code_id)

# ---------------------- ADD ZIP CODES ----------------------------------

    @check_connection
    def add_zip_code(self, zip_code: int, city_id: int) -> None:  # pragma: no cover
        with psycopg.connect(self._connection_url) as conn:
            queries.add_zip_code(conn, zip_code=zip_code, city_id=city_id)

# --------------------- DELETE ZIP CODES ---------------------------------

    @check_connection
    def delete_all_zip_codes(self) -> None:  # pragma: no cover
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

    @check_connection
    def get_make_by_id(self, make_id: int) -> dict:
        with psycopg.connect(self._connection_url, row_factory=dict_row) as conn:
            return queries.get_make_by_id(conn, id=make_id)

# --------------------- ADD MAKES ---------------------------------

    @check_connection
    def add_make(self, make_name: str) -> None:
        with psycopg.connect(self._connection_url) as conn:
            queries.add_make(conn, make_name=make_name)

# --------------------- DELETE MAKES ------------------------------

    @check_connection
    def delete_all_makes(self) -> None:  # pragma: no cover
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

    @check_connection
    def get_body_style_by_id(self, body_style_id: int) -> dict:
        with psycopg.connect(self._connection_url, row_factory=dict_row) as conn:
            return queries.get_body_style_by_id(conn, id=body_style_id)

# ------------------- ADD BODY STYLES ----------------------------

    @check_connection
    def add_body_style(self, body_style_name: str) -> None:
        with psycopg.connect(self._connection_url, row_factory=dict_row) as conn:
            queries.add_body_style(conn, body_style_name=body_style_name)

# ------------------ DELETE BODY STYLES --------------------------

    @check_connection
    def delete_all_body_styles(self) -> None:  # pragma: no cover
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

    @check_connection
    def get_model_count(self) -> int:
        with psycopg.connect(self._connection_url) as conn:
            return queries.get_model_count(conn)

    @check_connection
    def get_model_by_name(self, model_name: str) -> dict:
        with psycopg.connect(self._connection_url, row_factory=dict_row) as conn:
            return queries.get_model_by_name(conn, model_name=model_name)

    @check_connection
    def get_model_by_id(self, model_id: int) -> dict:
        with psycopg.connect(self._connection_url, row_factory=dict_row) as conn:
            return queries.get_model_by_id(conn, id=model_id)

# ---------------------------- ADD MODEL -------------------------------------

    @check_connection
    def add_model(self, model_name: str, make_id: int, body_style_id: int) -> None:
        with psycopg.connect(self._connection_url, row_factory=dict_row) as conn:
            queries.add_model(conn, model_name=model_name,
                              make_id=make_id, body_style_id=body_style_id)

    @check_connection
    def add_models(self, models_list: list[dict]) -> None:
        with psycopg.connect(self._connection_url, row_factory=dict_row) as conn:
            with conn.cursor() as cur:
                query = sql.SQL(
                    "INSERT INTO model(model_name, make_id, body_style_id) VALUES (%(model_name)s, %(make_id)s, %(body_style_id)s);")
                cur.executemany(query, models_list)

# ---------------------------- DELETE MODELS -------------------------------

    @check_connection
    def delete_all_models(self) -> None:  # pragma: no cover
        with psycopg.connect(self._connection_url, row_factory=dict_row) as conn:
            queries.delete_all_models(conn)

    @check_connection
    def delete_model_by_model_name(self, model_name: str) -> None:
        with psycopg.connect(self._connection_url, row_factory=dict_row) as conn:
            queries.delete_model_by_model_name(conn, model_name=model_name)


# ------------------------ WATCHED CAR -------------------------------------

# ------------------------ WATCHED CAR GET ---------------------------------

    @check_connection
    def get_all_watched_cars(self) -> list[dict]:
        with psycopg.connect(self._connection_url, row_factory=dict_row) as conn:
            return [car for car in queries.get_all_watched_cars(conn)]

    @check_connection
    def get_watched_car_by_vin(self, vin: str) -> dict:
        with psycopg.connect(self._connection_url, row_factory=dict_row) as conn:
            return queries.get_watched_car_by_vin(conn, vin=vin)

    @check_connection
    def get_watched_car_by_id(self, id: int) -> dict:
        with psycopg.connect(self._connection_url, row_factory=dict_row) as conn:
            return queries.get_watched_car_by_id(conn, id=id)

# ----------------------- ADD WATCHED CAR ----------------------------------

    @check_connection
    def add_watched_car(self, vin: str, listing_url: str, last_price: int, criteria_id: int, model_year: int) -> None:
        with psycopg.connect(self._connection_url, row_factory=dict_row) as conn:
            queries.add_watched_car(
                conn, vin=vin, listing_url=listing_url, last_price=last_price, criteria_id=criteria_id, model_year=model_year)

# ----------------------- UPDATE WATCHED CAR --------------------------------

    @check_connection
    def update_watched_car(self, vin: str, last_price: int, last_update: datetime, prev_price: int) -> None:
        with psycopg.connect(self._connection_url) as conn:
            queries.update_watched_car(
                conn, vin=vin, last_price=last_price, last_update=last_update, prev_price=prev_price)

# ---------------------- DELETE WATCHED CARS -------------------------------

    @check_connection
    def delete_all_watched_cars(self) -> None:
        with psycopg.connect(self._connection_url, row_factory=dict_row) as conn:
            queries.delete_all_watched_cars(conn)

    @check_connection
    def delete_watched_car_by_vin(self, vin: str) -> None:
        with psycopg.connect(self._connection_url, row_factory=dict_row) as conn:
            queries.delete_watched_car_by_vin(conn, vin=vin)

# --------------------- CRITERIA -------------------------------------------

# ------------------------ GET CRITERIA ------------------------------------

    @check_connection
    def get_all_criteria(self) -> list[dict]:
        with psycopg.connect(self._connection_url, row_factory=dict_row) as conn:
            return [criteria for criteria in queries.get_all_criteria(conn)]

    @check_connection
    def get_criteria_by_info(self,
                             min_year: int | None = None,
                             max_year: int | None = None,
                             min_price: int | None = None,
                             max_price: int | None = None,
                             max_mileage: int | None = None,
                             search_distance: int | None = None,
                             no_accidents: bool | None = True,
                             single_owner: bool | None = False,
                             user_id: int | None = None,
                             zip_code_id: int | None = None,
                             model_id: int | None = None,
                             body_style_id: int | None = None
                             ) -> list[dict]:
        with psycopg.connect(self._connection_url, row_factory=dict_row) as conn:
            res = queries.get_criteria_by_info(conn,
                                               min_year=min_year,
                                               max_year=max_year,
                                               min_price=min_price,
                                               max_price=max_price,
                                               max_mileage=max_mileage,
                                               search_distance=search_distance,
                                               no_accidents=no_accidents,
                                               single_owner=single_owner,
                                               user_id=user_id,
                                               zip_code_id=zip_code_id,
                                               model_id=model_id,
                                               body_style_id=body_style_id)

            return [criteria for criteria in res]

    @check_connection
    def get_criteria_by_id(self, id: int) -> dict:
        with psycopg.connect(self._connection_url, row_factory=dict_row) as conn:
            return queries.get_criteria_by_id(conn, id=id)

    @check_connection
    def get_criteria_by_user_id(self, user_id: int) -> list[dict]:
        with psycopg.connect(self._connection_url, row_factory=dict_row) as conn:
            res = queries.get_criteria_by_user_id(conn, user_id=user_id)
            return [criteria for criteria in res]

# ------------------------------- ADD CRITERIA ----------------------------------

    @check_connection
    def add_criteria(self,
                     min_year: int,
                     max_year: int,
                     min_price: int,
                     max_price: int,
                     max_mileage: int,
                     search_distance: int,
                     no_accidents: bool,
                     single_owner: bool,
                     user_id: int,
                     zip_code_id: int,
                     model_id: int,
                     body_style_id: int
                     ) -> None:
        with psycopg.connect(self._connection_url, row_factory=dict_row) as conn:
            queries.add_criteria(conn,

                                 min_year=min_year,
                                 max_year=max_year,
                                 min_price=min_price,
                                 max_price=max_price,
                                 max_mileage=max_mileage,
                                 search_distance=search_distance,
                                 no_accidents=no_accidents,
                                 single_owner=single_owner,
                                 user_id=user_id,
                                 zip_code_id=zip_code_id,
                                 model_id=model_id,
                                 body_style_id=body_style_id)

# --------------------- DELETE CRITERIA ------------------------------------------

    @check_connection
    def delete_all_criteria(self) -> None:
        with psycopg.connect(self._connection_url, row_factory=dict_row) as conn:
            queries.delete_all_criteria(conn)

    @check_connection
    def delete_criteria_by_info(self,
                                id: int | None = None,
                                min_year: int | None = None,
                                max_year: int | None = None,
                                min_price: int | None = None,
                                max_price: int | None = None,
                                max_mileage: int | None = None,
                                search_distance: int | None = None,
                                no_accidents: bool | None = True,
                                single_owner: bool | None = False,
                                user_id: int | None = None,
                                zip_code_id: int | None = None,
                                model_id: int | None = None,
                                body_style_id: int | None = None
                                ) -> None:

        with psycopg.connect(self._connection_url, row_factory=dict_row) as conn:
            queries.delete_criteria_by_info(conn,
                                            id=id,
                                            min_year=min_year,
                                            max_year=max_year,
                                            min_price=min_price,
                                            max_price=max_price,
                                            max_mileage=max_mileage,
                                            search_distance=search_distance,
                                            no_accidents=no_accidents,
                                            single_owner=single_owner,
                                            user_id=user_id,
                                            zip_code_id=zip_code_id,
                                            model_id=model_id,
                                            body_style_id=body_style_id)


# ----------------------------- Listing Alerts --------------------------------------

    @check_connection
    def get_all_alerts(self) -> list[dict]:
        with psycopg.connect(self._connection_url, row_factory=dict_row) as conn:
            return [row for row in queries.get_all_alerts(conn)]

    @check_connection
    def get_alert_by_info(self, car_id: int | None):
        with psycopg.connect(self._connection_url, row_factory=dict_row) as conn:
            return [row for row in queries.get_alerts_by_info(conn, car_id=car_id)]

    @check_connection
    def add_alert(self, car_id: int, change: str) -> None:
        with psycopg.connect(self._connection_url, row_factory=dict_row) as conn:
            queries.add_alert(conn, car_id=car_id, change=change)

    @check_connection
    def delete_all_alerts(self) -> None:
        with psycopg.connect(self._connection_url, row_factory=dict_row) as conn:
            queries.delete_all_alerts(conn)

    @check_connection
    def delete_alerts_by_info(self, car_id: int | None) -> None:
        with psycopg.connect(self._connection_url) as conn:
            queries.delete_alerts_by_info(conn, car_id=car_id)


# ----------------------- States -------------------------------------------------


    @check_connection
    def get_all_states(self) -> list[dict]:
        with psycopg.connect(self._connection_url, row_factory=dict_row) as conn:
            return [row for row in queries.get_all_states(conn)]

    @check_connection
    def get_state_by_name(self, state_name: str) -> dict | None:
        with psycopg.connect(self._connection_url, row_factory=dict_row) as conn:
            return queries.get_state_by_name(conn, state_name=state_name)

    @check_connection
    def add_state(self, state_name: str) -> None:  # pragma: no cover
        with psycopg.connect(self._connection_url, row_factory=dict_row) as conn:
            queries.add_state(conn, state_name=state_name)

    @check_connection
    def delete_all_states(self) -> None:  # pragma: no cover
        with psycopg.connect(self._connection_url, row_factory=dict_row) as conn:
            queries.delete_all_states(conn)
