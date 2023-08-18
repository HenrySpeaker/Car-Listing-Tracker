import pytest
from db.dbi.db_interface import DBInterface
from db.body_styles import body_styles
from config import DevConfig
import string
import random
from random import choice

DB_URI = DevConfig.POSTGRES_DATABASE_URI
WEBSITE_NAMES = ["autotrader", "cargurus", "usnews", "driveway", "capitolone"]
LISTING_CHANGES = ["price_drop", "new_listing"]
NUM_ZIPS = 33788
TEST_MODELS = ["Corvette", "Caliber", "Elantra", "Galant"]


def get_random_string(min_len: int, max_len: int) -> str:
    return "".join(random.choices(string.ascii_letters, k=random.randint(min_len, max_len)))


def get_tuple_from_dict(dict_in: dict):
    return tuple(dict_in[key] if dict_in[key] != None else 0 for key in sorted(dict_in.keys()) if key != "id")


def compare_data(data1: list[dict], data2: list[dict]):  # pragma: no cover
    if len(data1) != len(data2):
        return False

    sorted_data1 = sorted(data1, key=get_tuple_from_dict)
    sorted_data2 = sorted(data2, key=get_tuple_from_dict)

    for i in range(len(data1)):
        for key in sorted_data1[i]:
            if key not in sorted_data2[i] or sorted_data1[i][key] != sorted_data2[i][key]:
                return False

    return True


@pytest.fixture
def user_list() -> list[dict]:
    return [{"username": f"username{i}", "email": f"user{i}@email.com", "password_hash": f"password_hash{i}", "notification_frequency": 7} for i in range(1, 6)]


@pytest.fixture(scope="session")
def city_list() -> list[dict]:
    dbi = DBInterface(DB_URI)
    return dbi.get_all_cities()


@pytest.fixture(scope="session")
def make_list() -> list[dict]:
    dbi = DBInterface(DB_URI)
    return dbi.get_all_makes()


@pytest.fixture(scope="session")
def model_list() -> list[dict]:
    dbi = DBInterface(DB_URI)
    return dbi.get_all_models()


@pytest.fixture
def watched_car_list() -> list[dict]:
    return [{"vin": get_random_string(10, 25), "listing_url": get_random_string(30, 100), "last_price": random.randint(100, 100000), "model_year": random.randint(1992, 2023)} for _ in range(random.randint(5, 10))]


@pytest.fixture(scope="session")
def state_list() -> list[dict]:
    dbi = DBInterface(DB_URI)
    return dbi.get_all_states()


def add_body_styles(dao: DBInterface) -> DBInterface:  # pragma: no cover
    for style in body_styles:
        if not dao.get_body_style_info(style):
            dao.add_body_style(style)

    return dao


def delete_all_data(curr_dao: DBInterface):
    curr_dao.delete_all_users()
    curr_dao.delete_all_watched_cars()
    curr_dao.delete_all_criteria()
    curr_dao.delete_all_alerts()


@pytest.fixture
def new_dbi() -> DBInterface:
    curr_dbi = DBInterface(DB_URI)
    delete_all_data(curr_dbi)

    yield curr_dbi

    delete_all_data(curr_dbi)


def add_users(dbi: DBInterface, users: list[dict]) -> list[DBInterface, list[dict]]:
    for user in users:
        dbi.add_user(user)

    return [dbi, users]


@pytest.fixture
def dbi_with_users(new_dbi: DBInterface, user_list: list) -> list[DBInterface, list]:

    return add_users(new_dbi, user_list)


@pytest.fixture
def dbi_with_makes(new_dbi: DBInterface, make_list: list) -> list[DBInterface, list]:
    return [new_dbi, make_list]


@pytest.fixture
def dbi_with_web_body_styles(new_dbi: DBInterface) -> list[DBInterface, list[dict]]:
    new_dbi.delete_all_website_body_styles()
    web_body_styles = []
    for body_style in new_dbi.get_all_body_styles():
        for website in WEBSITE_NAMES:
            new_name = get_random_string(3, 10)
            new_dbi.add_website_body_style(
                body_style_id=body_style["id"], website_name=website, website_body_name=new_name)
            web_body_styles.append(
                {"website_name": website, "new_name": new_name, "body_style_id": body_style["id"]})

    return [new_dbi, web_body_styles]


@pytest.fixture
def dbi_with_models(new_dbi: DBInterface, make_list: list[dict], model_list) -> list[DBInterface, list[dict], list[dict]]:

    return [new_dbi, make_list, model_list]


def add_watched_cars(dbi: DBInterface, watched_cars: list[dict]) -> list[DBInterface, list]:
    all_criteria = dbi.get_all_criteria()
    for car in watched_cars:
        dbi.add_watched_car(
            vin=car["vin"], listing_url=car["listing_url"], last_price=car["last_price"], criteria_id=choice(all_criteria)["id"], model_year=car["model_year"])

    return [dbi, watched_cars]


@pytest.fixture
def dbi_with_watched_cars(dbi_with_criteria: list[DBInterface, list[dict], list[dict], list[dict], list[dict], list[dict]], watched_car_list: list[dict]):
    dao, criteria, makes, models, users, state_list = dbi_with_criteria
    return add_watched_cars(dao, watched_car_list)


def criteria_list(body_styles: list[dict], zips: list[dict], models: list[dict], users: list[dict]) -> list[dict]:
    criteria = []

    for _ in range(random.randint(5, 11)):
        new_criteria = {}

        new_criteria["min_year"] = random.choice(
            (random.randint(1980, 2020), None))
        new_criteria["max_year"] = random.choice(
            (random.randint(2021, 2024), None))
        new_criteria["min_year"] = random.choice(
            (random.randint(1980, 2020), None))
        new_criteria["min_price"] = random.choice(
            (random.randint(1000, 10000), None))
        new_criteria["max_price"] = random.choice(
            (random.randint(20000, 200000), None))
        new_criteria["max_mileage"] = random.choice(
            (random.randint(20000, 200000), None))
        new_criteria["search_distance"] = random.choice(
            (random.randint(5, 100), None))
        new_criteria["no_accidents"] = random.choice((True, False, None))
        new_criteria["single_owner"] = random.choice((True, False, None))
        new_criteria["user_id"] = random.choice(users)["id"]
        new_criteria["zip_code_id"] = random.choice(zips)["id"]

        if random.randint(0, 1) == 0:
            new_criteria["model_id"] = random.choice(models)["id"]
            new_criteria["body_style_id"] = None
        else:
            new_criteria["body_style_id"] = random.choice(body_styles)["id"]
            new_criteria["model_id"] = None

        criteria.append(new_criteria)

    return criteria


def add_criteria(dbi: DBInterface, criteria_list: list[dict]) -> list[DBInterface, list[dict]]:
    for criteria in criteria_list:
        dbi.add_criteria(
            min_year=criteria["min_year"],
            max_year=criteria["max_year"],
            min_price=criteria["min_price"],
            max_price=criteria["max_price"],
            max_mileage=criteria["max_mileage"],
            search_distance=criteria["search_distance"],
            no_accidents=criteria["no_accidents"],
            single_owner=criteria["single_owner"],
            user_id=criteria["user_id"],
            zip_code_id=criteria["zip_code_id"],
            model_id=criteria["model_id"],
            body_style_id=criteria["body_style_id"]
        )

    return [dbi, criteria_list]


@pytest.fixture
def dbi_with_criteria(new_dbi: DBInterface, make_list: list[dict], user_list: list[dict], state_list: list[dict], model_list) -> list[DBInterface, list[dict], list[dict], list[dict], list[dict], list[dict], list[dict]]:
    new_dbi = add_body_styles(new_dbi)

    new_dbi, user_list = add_users(new_dbi, user_list)

    criteria = criteria_list(new_dbi.get_all_body_styles(
    ), new_dbi.get_all_zip_codes(), new_dbi.get_all_models(), new_dbi.get_all_users())

    new_dbi, criteria = add_criteria(new_dbi, criteria)

    return [new_dbi, criteria, make_list, model_list, user_list, state_list]


def add_watched_car_criteria(dbi: DBInterface) -> list[DBInterface, list[dict], list[dict]]:
    watched_car_criteria = []
    criteria = dbi.get_all_criteria()
    watched_cars = dbi.get_all_watched_cars()
    pairs_seen = set()
    for _ in range(random.randint(5, 15)):
        new_row = {"criteria_id": random.choice(
            criteria)["id"], "watched_car_id": random.choice(watched_cars)["id"]}
        if (new_row["criteria_id"], new_row["watched_car_id"]) not in pairs_seen:
            dbi.add_watched_car_criteria(**new_row)
            watched_car_criteria.append(new_row)
            pairs_seen.add((new_row["criteria_id"], new_row["watched_car_id"]))

    return [dbi, watched_car_criteria]


@pytest.fixture
def dbi_with_watched_car_criteria(dbi_with_criteria: list[DBInterface, list[dict], list[dict], list[dict], list[dict], list[dict]], watched_car_list: list[dict]) -> list[DBInterface, list[dict], list[dict], list[dict], list[dict], list[dict], list[dict], list[dict]]:
    new_dbi, criteria, make_list, models_list, user_list, states = dbi_with_criteria

    new_dbi, watched_cars = add_watched_cars(new_dbi, watched_car_list)

    new_dbi, watched_car_criteria = add_watched_car_criteria(new_dbi)

    return [new_dbi, criteria, make_list, models_list, user_list, watched_cars, watched_car_criteria]


def add_listing_alerts(dbi: DBInterface) -> list[DBInterface, list[dict]]:
    dbi.delete_all_alerts()
    new_alerts = []
    user_list = dbi.get_all_users()
    watched_car_list = dbi.get_all_watched_cars()

    def add_type_alerts(type):

        for _ in range(random.randint(5, 10)):
            new_alert = {}
            new_alert["car_id"] = random.choice(watched_car_list)["id"]
            new_alert["change"] = random.choice(LISTING_CHANGES)
            new_alerts.append(new_alert)

            dbi.add_alert(**new_alert)

    for type in LISTING_CHANGES:
        add_type_alerts(type)

    return [dbi, new_alerts]


@pytest.fixture
def dbi_with_listing_alerts(dbi_with_criteria: list[DBInterface, list[dict], list[dict], list[dict], list[dict], list[dict]], watched_car_list: list[dict]):
    dbi, criteria, makes, models, users, state_list = dbi_with_criteria
    dbi, watched_car_list = add_watched_cars(dbi, watched_car_list)
    dbi, listing_alerts = add_listing_alerts(dbi)
    return [dbi, users, watched_car_list, listing_alerts]


def add_states(dbi: DBInterface, states: list[dict]) -> list[DBInterface, list[dict]]:
    return [dbi, states]


@pytest.fixture
def dbi_with_states(new_dbi: DBInterface, state_list: list[dict]) -> list[DBInterface, list[dict]]:
    return add_states(new_dbi, state_list)
