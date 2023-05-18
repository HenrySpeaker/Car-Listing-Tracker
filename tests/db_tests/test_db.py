import pytest
from db.dao.db_interface import DBInterface
from config import DevConfig
from datetime import datetime

DB_URI = DevConfig.POSTGRES_DATABASE_URI


@pytest.fixture
def user_list():
    return [{"username": f"username{i}", "email": f"user{i}@email.com", "password_hash": f"password_hash{i}", "notification_frequency": 7} for i in range(1, 6)]


@pytest.fixture
def new_dao() -> DBInterface:
    curr_dao = DBInterface(DB_URI)
    curr_dao.delete_all_users()
    return curr_dao


@pytest.fixture
def dao_with_users(new_dao: DBInterface, user_list: list) -> list[DBInterface, list]:
    for user in user_list:
        new_dao.add_user(user)

    return [new_dao, user_list]


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
