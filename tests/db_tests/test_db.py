import random
from random import choice, choices
from datetime import datetime
from collections import defaultdict
import pytest
from pytz import timezone
import psycopg
from db.dbi.db_interface import DBInterface
from db.body_styles import body_styles
from config import ZIP_ROW_COUNT
from tests.utils.db_utils import *  # noqa: F403


def test_false_valid_connection_attribute(new_dbi: DBInterface):
    with pytest.raises(RuntimeError) as excinfo:
        new_dbi._valid_connection = False
        res = new_dbi.get_all_users()

    assert "The database connection is not valid." in str(excinfo.value)

    new_dbi._valid_connection = True


def test_bad_db_url(capsys):
    curr_dao = DBInterface("Not a valid db url")
    assert capsys.readouterr().out == 'An error occurred: missing "=" after "Not" in connection info string\n\n'


def test_get_user_by_id(dbi_with_users: list[DBInterface, list]):
    dao, users = dbi_with_users
    users_list = dao.get_all_users()

    for user in users_list:
        poss_match = dao.get_user_by_id(user["id"])
        for key in user:
            assert user[key] == poss_match[key]


def test_add_user(new_dbi, user_list):
    for user in user_list:
        new_dbi.add_user(user)

    all_users = new_dbi.get_all_users()

    assert len(all_users) == len(user_list)


def test_get_user_by_username(dbi_with_users: list[DBInterface, list]):
    dao, user_list = dbi_with_users

    assert dao.get_user_by_username(user_list[0]["username"])[
        "username"] == user_list[0]["username"]


def test_get_user_by_invalid_username(dbi_with_users: list[DBInterface, list]):
    dao, user_list = dbi_with_users

    assert dao.get_user_by_username("Not a username") == None


def test_get_user_by_email(dbi_with_users: list[DBInterface, list]):
    dao, user_list = dbi_with_users

    assert dao.get_user_by_email(user_list[0]["email"])[
        "email"] == user_list[0]["email"]


def test_get_user_by_invalid_email(dbi_with_users: list[DBInterface, list]):
    dao, user_list = dbi_with_users

    assert dao.get_user_by_email("Not an email") == None


def test_update_user_by_email(dbi_with_users: list[DBInterface, list]):
    dao, user_list = dbi_with_users
    NEW_USERNAME = "new username"
    user_email = user_list[0]["email"]
    dao.update_username_by_email(
        email=user_email, new_username=NEW_USERNAME)

    assert dao.get_user_by_email(user_email)["username"] == NEW_USERNAME


def test_update_email_by_username(dbi_with_users: list[DBInterface, list]):
    dao, user_list = dbi_with_users
    NEW_EMAIL = "new@email.com"
    username = user_list[0]["username"]
    dao.update_email_by_username(
        new_email=NEW_EMAIL, username=username)

    assert dao.get_user_by_username(username)["email"] == NEW_EMAIL


def test_update_password_hash_by_username(dbi_with_users: list[DBInterface, list]):
    dao, user_list = dbi_with_users
    NEW_PASSWORD_HASH = "new password hash"
    username = user_list[0]["username"]
    dao.update_password_hash_by_username(
        username=username, new_password_hash=NEW_PASSWORD_HASH)

    assert dao.get_user_by_username(
        username)["password_hash"] == NEW_PASSWORD_HASH


def test_update_notification_frequency_by_username(dbi_with_users: list[DBInterface, list]):
    dao, user_list = dbi_with_users
    NEW_NOTIFICATION_FREQUENCY = 20
    username = user_list[0]["username"]
    dao.update_notification_frequency_by_username(
        username=username, new_notification_frequency=NEW_NOTIFICATION_FREQUENCY)

    assert dao.get_user_by_username(
        username)["notification_frequency"] == NEW_NOTIFICATION_FREQUENCY


def test_update_last_login_by_username(dbi_with_users: list[DBInterface, list]):
    dao, user_list = dbi_with_users
    new_login_dt = datetime.now(timezone("UTC"))
    username = user_list[0]["username"]
    dao.update_last_login_by_username(
        username=username, login_datetime=new_login_dt)

    new_last_login = dao.get_user_by_username(username)["last_login"]

    # the database returns an aware datetime object so the timezone used by the database must be determined and then the new_login_dt adjusted to that timezone
    last_login_tz = new_last_login.tzinfo
    assert new_last_login == new_login_dt.astimezone(last_login_tz)


def test_update_last_alerted_by_id(dbi_with_users: list[DBInterface, list]):
    dao, user_list = dbi_with_users
    new_alert_dt = datetime.now(timezone("UTC"))
    user_id = dao.get_all_users()[0]["id"]
    dao.update_last_alerted_by_id(id=user_id, last_alerted=new_alert_dt)

    alert_time = dao.get_user_by_id(id=user_id)["last_alerted"]

    # the database returns an aware datetime object so the timezone used by the database must be determined and then the new_login_dt adjusted to that timezone
    last_alert_tz = alert_time.tzinfo
    assert alert_time == new_alert_dt.astimezone(last_alert_tz)


def test_delete_user_by_username(dbi_with_users: list[DBInterface, list]):
    dao, user_list = dbi_with_users

    for user in user_list:
        dao.delete_user_by_username(user["username"])

    assert len(dao.get_all_users()) == 0


def test_get_all_cities(new_dbi: DBInterface, city_list: list[dict]):
    all_cities = new_dbi.get_all_cities()
    all_cities_set = set(city["city_name"] for city in all_cities)

    assert len(all_cities) == len(city_list)


def test_delete_cities_by_name(new_dbi: DBInterface, city_list: list[dict]):
    TEST_CITY = "Not a city"
    TEST_STATE_ID = new_dbi.get_state_by_name("New York")["id"]
    new_dbi.add_city(city_name=TEST_CITY, state_id=TEST_STATE_ID)

    assert new_dbi.get_city_id(TEST_CITY) != None

    new_dbi.delete_city_by_name(TEST_CITY)

    assert new_dbi.get_city_id(TEST_CITY) == None


def test_get_city_id(new_dbi: DBInterface, city_list: list[dict]):
    all_cities = new_dbi.get_all_cities()
    for city in choices(all_cities, k=10):
        returned_city_id = new_dbi.get_city_id(city["city_name"])
        assert city["id"] == returned_city_id


def test_get_all_zip_codes(new_dbi: DBInterface):
    dao = new_dbi
    all_zips = dao.get_all_zip_codes()
    assert len(all_zips) == NUM_ZIPS


def test_get_zip_code_info(new_dbi: DBInterface):
    test_zip = 90210
    data = new_dbi.get_zip_code_info(zip_code=test_zip)
    assert data["zip_code"] == test_zip


def test_get_zip_count(new_dbi: DBInterface):
    assert new_dbi.get_zip_code_count() == ZIP_ROW_COUNT


def test_get_zip_code_by_id(new_dbi: DBInterface):
    test_zips = choices(new_dbi.get_all_zip_codes(), k=5)

    for zip in test_zips:
        assert zip["zip_code"] == new_dbi.get_zip_code_by_id(zip["id"])[
            "zip_code"]


def test_delete_specific_zip(new_dbi: DBInterface):
    dao = new_dbi

    false_zip = 1
    test_city = "Not a city"
    test_state_id = dao.get_state_by_name("New York")["id"]
    dao.add_city(city_name=test_city, state_id=test_state_id)
    city_id = dao.get_city_id(test_city)
    dao.add_zip_code(zip_code=false_zip, city_id=city_id)

    assert dao.get_zip_code_info(false_zip) != {}

    dao.delete_zip_code(false_zip)

    assert dao.get_zip_code_info(false_zip) == None


def test_get_all_makes(new_dbi: DBInterface):
    all_makes = new_dbi.get_all_makes()

    assert len(all_makes) == 66


def test_get_specific_makes(dbi_with_makes: list[DBInterface, list]):
    dao, makes_list = dbi_with_makes
    makes_list = dao.get_all_makes()

    for make in makes_list:
        make_info = dao.get_make_info(make["make_name"])
        assert len(
            make_info) == 2 and make_info["make_name"] == make["make_name"]


def test_get_make_by_id(new_dbi: DBInterface):

    all_makes = new_dbi.get_all_makes()

    for make in all_makes:
        assert new_dbi.get_make_by_id(
            make["id"])["make_name"] == make["make_name"]


def test_add_and_remove_make(new_dbi: DBInterface):
    test_make = get_random_string(3, 8)
    new_dbi.add_make(test_make)

    assert new_dbi.get_make_info(test_make) != {}

    new_dbi.delete_make_by_name(test_make)

    assert new_dbi.get_make_info(test_make) == None


def test_get_all_body_styles(new_dbi: DBInterface):
    res = new_dbi.get_all_body_styles()

    for res_body_style in res:
        assert res_body_style["body_style_name"] in body_styles


def test_get_specific_body_style(new_dbi: DBInterface):
    for style in body_styles:
        assert new_dbi.get_body_style_info(
            style)["body_style_name"] == style


def test_get_body_style_by_id(new_dbi: DBInterface):
    res = new_dbi.get_all_body_styles()

    for body_style in res:
        assert new_dbi.get_body_style_by_id(
            body_style["id"])["body_style_name"] == body_style["body_style_name"]


def test_add_invalid_body_style(new_dbi: DBInterface):
    with pytest.raises(psycopg.errors.InvalidTextRepresentation):
        new_dbi.add_body_style("not a valid body style")


def test_get_all_web_body_styles(dbi_with_web_body_styles: list[DBInterface, list[dict]]):
    dao, web_body_styles = dbi_with_web_body_styles
    all_web_body_styles = dao.get_all_website_body_styles()

    assert len(all_web_body_styles) == len(body_styles) * len(WEBSITE_NAMES)

    web_body_style_names = set(
        web_body_style["new_name"] for web_body_style in web_body_styles)

    for style in all_web_body_styles:
        assert style["website_body_name"] in web_body_style_names


def test_get_specific_web_body_style(dbi_with_web_body_styles: list[DBInterface, list[dict]]):
    dao, web_body_styles = dbi_with_web_body_styles
    print(web_body_styles)

    for web_body_style in web_body_styles:
        retrieved_web_body_styles = dao.get_website_body_style_info(
            web_body_style["body_style_id"])

        assert len(retrieved_web_body_styles) == len(WEBSITE_NAMES)


def test_delete_specific_web_body_style(dbi_with_web_body_styles: list[DBInterface, list[dict]]):
    dao, web_body_styles = dbi_with_web_body_styles

    assert len(dao.get_all_website_body_styles()) == len(
        body_styles) * len(WEBSITE_NAMES)

    for web_body_style in web_body_styles:
        dao.delete_specific_website_body_style(web_body_style["body_style_id"])

    assert len(dao.get_all_website_body_styles()) == 0


def test_get_all_models(dbi_with_models: list[DBInterface, list[dict], list[dict]]):
    dao, make_list, models_list = dbi_with_models

    all_models_from_dao = dao.get_all_models()
    model_names_from_dao = {model["model_name"]
                            for model in all_models_from_dao}

    assert len(all_models_from_dao) == len(models_list)

    for model in models_list:
        assert model["model_name"] in model_names_from_dao


def test_get_model_by_make_id(dbi_with_models: list[DBInterface, list[dict], list[dict]]):
    dao, make_list, models_list = dbi_with_models

    models_by_make_id = defaultdict(list)

    for model in models_list:
        models_by_make_id[model["make_id"]].append(model)

    for make_id in models_by_make_id:
        dao_models_by_make_id = dao.get_models_by_make_id(make_id)
        assert len(dao_models_by_make_id) == len(models_by_make_id[make_id])

        for dao_model in dao_models_by_make_id:
            assert dao_model["make_id"] == make_id


def test_get_model_by_make_name(dbi_with_models: list[DBInterface, list[dict], list[dict]]):
    dao, make_list, models_list = dbi_with_models

    dao_make_info = dao.get_all_makes()

    models_by_make_id = defaultdict(list)

    for model in models_list:
        models_by_make_id[model["make_id"]].append(model)

    for make in dao_make_info:
        assert len(dao.get_model_by_make_name(make["make_name"])) == len(
            models_by_make_id[make["id"]])


def test_get_model_by_body_style_id(dbi_with_models: list[DBInterface, list[dict], list[dict]]):
    dao, make_list, models_list = dbi_with_models

    body_style_info = dao.get_all_body_styles()

    models_by_body_style = defaultdict(list)

    for model in models_list:
        models_by_body_style[model["body_style_id"]].append(model)

    for body_style in body_style_info:
        assert len(models_by_body_style[body_style["id"]]) == len(
            dao.get_model_by_body_style_id(body_style["id"]))


def test_get_model_by_body_style_name(dbi_with_models: list[DBInterface, list[dict], list[dict]]):
    dao, make_list, models_list = dbi_with_models

    body_style_info = dao.get_all_body_styles()
    models_by_body_style = defaultdict(list)

    for model in models_list:
        models_by_body_style[model["body_style_id"]].append(model)

    for body_style in body_style_info:
        assert len(models_by_body_style[body_style["id"]]) == len(
            dao.get_model_by_body_style_name(body_style["body_style_name"]))


def test_get_model_count(dbi_with_models: list[DBInterface, list[dict], list[dict]]):
    dao, make_list, models_list = dbi_with_models

    assert dao.get_model_count() == len(models_list)


def test_get_model_by_name(dbi_with_models: list[DBInterface, list[dict], list[dict]]):
    dao, make_list, models_list = dbi_with_models
    models_list = choices([model["model_name"]
                          for model in dao.get_all_models()], k=5)
    for model_name in models_list:
        assert dao.get_model_by_name(model_name) != None


def test_get_model_by_id(dbi_with_models: list[DBInterface, list[dict], list[dict]]):
    dao, make_list, models_list = dbi_with_models

    models_list = choices([model for model in dao.get_all_models()], k=5)

    for model in models_list:
        assert dao.get_model_by_id(model["id"])[
            "model_name"] == model["model_name"]


def test_add_model(new_dbi: DBInterface):
    makes = new_dbi.get_all_makes()
    body_style_data = new_dbi.get_all_body_styles()

    rand_make = choice(makes)
    rand_style = choice(body_style_data)

    new_model = {"model_name": get_random_string(
        5, 10), "make_id": rand_make["id"], "body_style_id": rand_style["id"]}

    new_dbi.add_model(**new_model)

    assert new_dbi.get_model_by_name(new_model["model_name"])[
        "model_name"] == new_model["model_name"]

    new_dbi.delete_model_by_model_name(new_model["model_name"])

    assert new_dbi.get_model_by_name(new_model["model_name"]) == None


def test_get_all_watched_cars(dbi_with_watched_cars: list[DBInterface, list[dict]]):
    dao, watched_cars = dbi_with_watched_cars

    dao_watched_cars = dao.get_all_watched_cars()

    dao_watched_car_vins = {car["vin"] for car in dao_watched_cars}

    assert len(dao_watched_cars) == len(watched_cars)

    for car in watched_cars:
        assert car["vin"] in dao_watched_car_vins


def test_get_watched_car_by_vin(dbi_with_watched_cars: list[DBInterface, list[dict]]):
    dao, watched_cars = dbi_with_watched_cars

    for car in watched_cars:
        dao_car = dao.get_watched_car_by_vin(car["vin"])
        assert dao_car["vin"] == car["vin"]
        assert dao_car["listing_url"] == car["listing_url"]
        assert dao_car["last_price"] == car["last_price"]


def test_get_watched_car_by_id(dbi_with_watched_cars: list[DBInterface, list[dict]]):
    dao, watched_cars = dbi_with_watched_cars

    db_watched_cars = dao.get_all_watched_cars()

    for car in db_watched_cars:
        res = dao.get_watched_car_by_id(id=car["id"])
        assert compare_data([car], [res])


def test_delete_watched_car_by_vin(dbi_with_watched_cars: list[DBInterface, list[dict]]):
    dao, watched_cars = dbi_with_watched_cars

    assert len(dao.get_all_watched_cars()) == len(watched_cars)

    for car in watched_cars:
        dao.delete_watched_car_by_vin(car["vin"])

    assert len(dao.get_all_watched_cars()) == 0


def test_update_watched_car(dbi_with_watched_cars: list[DBInterface, list[dict]]):
    dao, watched_cars = dbi_with_watched_cars
    curr_time = datetime.now(timezone("UTC"))
    new_price = random.randint(100, 500000)

    for car in watched_cars:
        dao.update_watched_car(
            vin=car["vin"], last_price=new_price, last_update=curr_time, prev_price=car["last_price"])

    for car in watched_cars:
        car_data = dao.get_watched_car_by_vin(car["vin"])
        last_update_tz = car_data["last_update"].tzinfo
        assert car_data["last_update"] == curr_time.astimezone(last_update_tz)
        assert car_data["last_price"] == new_price
        assert car_data["prev_price"] == car["last_price"]


def test_get_all_criteria(dbi_with_criteria: list[DBInterface, list[dict], list[dict], list[dict], list[dict], list[dict]]):
    dao, criteria, makes, models, users, state_list = dbi_with_criteria

    db_criteria = dao.get_all_criteria()
    assert len(db_criteria) == len(criteria)

    for crit in db_criteria:
        crit.pop("id")

    assert compare_data(criteria, db_criteria)


def test_get_criteria_by_info(dbi_with_criteria: list[DBInterface, list[dict], list[dict], list[dict], list[dict], list[dict]]):
    dao, criteria, makes, models, users, state_list = dbi_with_criteria

    identical_criteria_count = defaultdict(int)

    for crit in criteria:
        identical_criteria_count[get_tuple_from_dict(crit)] += 1

    for crit in criteria:
        db_criteria = dao.get_criteria_by_info(**crit)
        assert len(
            db_criteria) == identical_criteria_count[get_tuple_from_dict(crit)]


def test_get_criteria_by_id(dbi_with_criteria: list[DBInterface, list[dict], list[dict], list[dict], list[dict], list[dict]]):
    dao, criteria, makes, models, users, state_list = dbi_with_criteria

    all_criteria = dao.get_all_criteria()

    for crit in all_criteria:
        assert get_tuple_from_dict(crit) == get_tuple_from_dict(
            dao.get_criteria_by_id(crit["id"]))


def test_get_criteria_by_user_id(dbi_with_criteria: list[DBInterface, list[dict], list[dict], list[dict], list[dict], list[dict]]):
    dao, criteria, makes, models, users, state_list = dbi_with_criteria

    user_crit_count = defaultdict(int)

    for crit in dao.get_all_criteria():
        user_crit_count[crit["user_id"]] += 1

    users_info = dao.get_all_users()

    for user in users_info:
        assert len(dao.get_criteria_by_user_id(
            user["id"])) == user_crit_count[user["id"]]


def test_delete_criteria_by_info(dbi_with_criteria: list[DBInterface, list[dict], list[dict], list[dict], list[dict], list[dict]]):
    dao, criteria, makes, models, users, state_list = dbi_with_criteria

    assert len(dao.get_all_criteria()) == len(criteria)

    for crit in criteria:
        dao.delete_criteria_by_info(**crit)

    assert len(dao.get_all_criteria()) == 0


def test_get_all_listing_alerts(dbi_with_listing_alerts: list[DBInterface, list[dict], list[dict], list[dict]]):
    dao, users, watched_cars, alerts = dbi_with_listing_alerts

    alerts_data = dao.get_all_alerts()

    assert len(alerts_data) == len(alerts)

    assert compare_data(alerts, alerts_data)


def test_get_listing_alerts_by_info(dbi_with_listing_alerts: list[DBInterface, list[dict], list[dict], list[dict]]):
    dao, users, watched_cars, alerts = dbi_with_listing_alerts

    for alert in alerts:
        get_res = dao.get_alert_by_info(car_id=alert["car_id"])
        assert len(get_res) >= 1
        res = get_res[0]
        assert res["car_id"] == alert["car_id"]


def test_delete_listing_alerts_by_info(dbi_with_listing_alerts: list[DBInterface, list[dict], list[dict], list[dict]]):
    dao, users, watched_cars, alerts = dbi_with_listing_alerts

    all_alerts = dao.get_all_alerts()

    assert len(all_alerts) == len(alerts)

    for alert in alerts:
        dao.delete_alerts_by_info(car_id=alert["car_id"])

    all_alerts = dao.get_all_alerts()

    assert len(all_alerts) == 0


def test_get_all_states(dbi_with_states: list[DBInterface, list[dict]]):
    dao, states = dbi_with_states

    states_data = dao.get_all_states()

    assert len(states_data) == len(states)

    assert compare_data(states, states_data)


def test_get_state_by_name(dbi_with_states: list[DBInterface, list[dict]]):
    dao, states = dbi_with_states

    for state in states:
        returned_data = dao.get_state_by_name(state["state_name"])
        assert returned_data != None
        assert returned_data["state_name"] == state["state_name"]

    assert dao.get_state_by_name(
        "*************** not a state *******************") == None
