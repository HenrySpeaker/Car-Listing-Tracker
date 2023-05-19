import pytest
from db.dao.db_interface import DBInterface
from config import DevConfig
from datetime import datetime
import string
import random

DB_URI = DevConfig.POSTGRES_DATABASE_URI


@pytest.fixture
def user_list():
    return [{"username": f"username{i}", "email": f"user{i}@email.com", "password_hash": f"password_hash{i}", "notification_frequency": 7} for i in range(1, 6)]


@pytest.fixture
def city_list():
    return [{"city_name": "".join(random.choices(string.ascii_letters, k=random.randint(3, 10)))} for _ in range(5)]


@pytest.fixture
def make_list():
    return [{"make_name": "".join(random.choices(string.ascii_letters, k=random.randint(3, 10)))} for _ in range(5)]


@pytest.fixture
def new_dao() -> DBInterface:
    curr_dao = DBInterface(DB_URI)
    curr_dao.delete_all_users()
    curr_dao.delete_all_cities()
    curr_dao.delete_all_makes()
    return curr_dao


@pytest.fixture
def dao_with_users(new_dao: DBInterface, user_list: list) -> list[DBInterface, list]:
    for user in user_list:
        new_dao.add_user(user)

    return [new_dao, user_list]


@pytest.fixture
def dao_with_cities(new_dao: DBInterface, city_list: list[dict]) -> list[DBInterface, list]:
    for city in city_list:
        new_dao.add_city(city["city_name"])

    return [new_dao, city_list]


@pytest.fixture
def dao_with_cities_and_zips(dao_with_cities: list[DBInterface, list]) -> list[DBInterface, list, list]:
    dao, city_list = dao_with_cities
    dao.delete_all_zip_codes()
    city_id_list = [city["id"] for city in dao.get_all_cities()]
    zips_list = [{"zip_code": random.randint(
        10000, 99999), "city_id": random.choice(city_id_list)}]

    for zip_code in zips_list:
        dao.add_zip_code(
            zip_code=zip_code["zip_code"], city_id=zip_code["city_id"])

    return [dao, city_list, zips_list]


@pytest.fixture
def dao_with_makes(new_dao: DBInterface, make_list: list) -> list[DBInterface, list]:
    for make in make_list:
        new_dao.add_make(make["make_name"])

    return [new_dao, make_list]


def test_bad_db_url(capsys):
    curr_dao = DBInterface("Not a valid db url")
    assert capsys.readouterr(
    ).out == 'An error occurred: missing "=" after "Not" in connection info string\n\n'


def test_add_user(new_dao, user_list):
    for user in user_list:
        new_dao.add_user(user)

    all_users = new_dao.get_all_users()

    assert len(all_users) == len(user_list)


def test_get_user_by_username(dao_with_users: list[DBInterface, list]):
    dao, user_list = dao_with_users

    assert dao.get_user_by_username(user_list[0]["username"])[
        "username"] == user_list[0]["username"]


def test_get_user_by_invalid_username(dao_with_users: list[DBInterface, list]):
    dao, user_list = dao_with_users

    assert dao.get_user_by_username("Not a username") == None


def test_get_user_by_email(dao_with_users: list[DBInterface, list]):
    dao, user_list = dao_with_users

    assert dao.get_user_by_email(user_list[0]["email"])[
        "email"] == user_list[0]["email"]


def test_get_user_by_invalid_email(dao_with_users: list[DBInterface, list]):
    dao, user_list = dao_with_users

    assert dao.get_user_by_email("Not an email") == None


def test_update_user_by_email(dao_with_users: list[DBInterface, list]):
    dao, user_list = dao_with_users
    NEW_USERNAME = "new username"
    user_email = user_list[0]["email"]
    dao.update_username_by_email(
        email=user_email, new_username=NEW_USERNAME)

    assert dao.get_user_by_email(user_email)["username"] == NEW_USERNAME


def test_update_email_by_username(dao_with_users: list[DBInterface, list]):
    dao, user_list = dao_with_users
    NEW_EMAIL = "new@email.com"
    username = user_list[0]["username"]
    dao.update_email_by_username(
        new_email=NEW_EMAIL, username=username)

    assert dao.get_user_by_username(username)["email"] == NEW_EMAIL


def test_update_password_hash_by_username(dao_with_users: list[DBInterface, list]):
    dao, user_list = dao_with_users
    NEW_PASSWORD_HASH = "new password hash"
    username = user_list[0]["username"]
    dao.update_password_hash_by_username(
        username=username, new_password_hash=NEW_PASSWORD_HASH)

    assert dao.get_user_by_username(
        username)["password_hash"] == NEW_PASSWORD_HASH


def test_update_notification_frequency_by_username(dao_with_users: list[DBInterface, list]):
    dao, user_list = dao_with_users
    NEW_NOTIFICATION_FREQUENCY = 20
    username = user_list[0]["username"]
    dao.update_notification_frequency_by_username(
        username=username, new_notification_frequency=NEW_NOTIFICATION_FREQUENCY)

    assert dao.get_user_by_username(
        username)["notification_frequency"] == NEW_NOTIFICATION_FREQUENCY


def test_update_last_login_by_username(dao_with_users: list[DBInterface, list]):
    dao, user_list = dao_with_users
    new_login_dt = datetime.now()
    username = user_list[0]["username"]
    dao.update_last_login_by_username(
        username=username, login_datetime=new_login_dt)

    new_last_login = dao.get_user_by_username(username)["last_login"]

    # the database returns an aware datetime object so the timezone used by the database must be determined and then the new_login_dt adjusted to that timezone
    last_login_tz = new_last_login.tzinfo
    assert new_last_login == new_login_dt.astimezone(last_login_tz)


def test_delete_user_by_username(dao_with_users: list[DBInterface, list]):
    dao, user_list = dao_with_users

    for user in user_list:
        dao.delete_user_by_username(user["username"])

    assert len(dao.get_all_users()) == 0


def test_get_all_cities(dao_with_cities: list[DBInterface, list]):
    dao, city_list = dao_with_cities
    all_cities = dao.get_all_cities()
    all_cities_set = set(city["city_name"] for city in all_cities)

    assert len(all_cities) == len(city_list)
    for city in city_list:
        assert city["city_name"] in all_cities_set


def test_delete_cities_by_name(dao_with_cities: list[DBInterface, list]):
    dao, city_list = dao_with_cities
    for city in city_list:
        dao.delete_city_by_name(city["city_name"])

    assert len(dao.get_all_cities()) == 0


def test_get_city_id(dao_with_cities: list[DBInterface, list]):
    dao, city_list = dao_with_cities
    all_cities = dao.get_all_cities()
    for city in all_cities:
        returned_city_id = dao.get_city_id(city["city_name"])
        assert city["id"] == returned_city_id


def test_get_all_zip_codes(dao_with_cities_and_zips: list[DBInterface, list, list]):
    dao, city_list, zip_list = dao_with_cities_and_zips

    assert len(dao.get_all_zip_codes()) == len(zip_list)


def test_get_specific_zip_codes(dao_with_cities_and_zips: list[DBInterface, list, list]):
    dao, city_list, zip_list = dao_with_cities_and_zips

    for zip_info in zip_list:
        assert dao.get_city_id_by_zip_code(
            zip_info["zip_code"]) == zip_info["city_id"]


def test_delete_specific_zip(dao_with_cities_and_zips: list[DBInterface, list, list]):
    dao, city_list, zip_list = dao_with_cities_and_zips

    assert len(dao.get_all_zip_codes()) > 0

    for zip_info in zip_list:
        dao.delete_zip_code(zip_info["zip_code"])

    assert len(dao.get_all_zip_codes()) == 0


def test_get_all_makes(dao_with_makes: list[DBInterface, list]):
    dao, makes_list = dao_with_makes
    makes_name_set = set(make["make_name"] for make in makes_list)
    all_makes = dao.get_all_makes()

    assert len(all_makes) == len(makes_list)

    for make in makes_list:
        assert make["make_name"] in makes_name_set


def test_get_specific_makes(dao_with_makes: list[DBInterface, list]):
    dao, makes_list = dao_with_makes

    for make in makes_list:
        make_info = dao.get_make_info(make["make_name"])
        assert len(
            make_info) == 2 and make_info["make_name"] == make["make_name"]


def test_delete_make_by_name(dao_with_makes: list[DBInterface, list]):
    dao, makes_list = dao_with_makes

    for make in makes_list:
        dao.delete_make_by_name(make["make_name"])

    assert len(dao.get_all_makes()) == 0
