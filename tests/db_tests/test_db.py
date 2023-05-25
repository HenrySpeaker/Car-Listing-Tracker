import pytest
from db.dao.db_interface import DBInterface
from db.body_styles import body_styles
from config import DevConfig
from datetime import datetime
import string
import random
import psycopg
from collections import defaultdict

DB_URI = DevConfig.POSTGRES_DATABASE_URI
WEBSITE_NAMES = ["autotrader", "truecar"]


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


@pytest.fixture
def city_list() -> list[dict]:
    return [{"city_name": get_random_string(3, 10)} for _ in range(5)]


@pytest.fixture
def make_list() -> list[dict]:
    return [{"make_name": get_random_string(3, 10)} for _ in range(5)]


@pytest.fixture
def watched_car_list() -> list[dict]:
    return [{"vin": get_random_string(10, 25), "listing_url": get_random_string(30, 100), "last_price": random.randint(100, 100000)} for _ in range(random.randint(5, 10))]


def add_body_styles(dao: DBInterface) -> DBInterface:
    dao.delete_all_body_styles()
    for style in body_styles:
        dao.add_body_style(style)

    return dao


def add_makes(dao: DBInterface, make_list: list[dict]) -> list[DBInterface, list]:
    for make in make_list:
        dao.add_make(make["make_name"])

    return [dao, make_list]


def add_models(dao: DBInterface) -> list[DBInterface, list[dict]]:
    all_makes = dao.get_all_makes()
    all_body_styles = dao.get_all_body_styles()
    new_models = []

    for _ in range(random.randint(3, 9)):
        new_model_name = get_random_string(3, 15)
        new_make_id = random.choice(all_makes)["id"]
        new_body_style_id = random.choice(all_body_styles)["id"]

        new_model = {"model_name": new_model_name,
                     "make_id": new_make_id, "body_style_id": new_body_style_id}
        new_models.append(new_model)

        dao.add_model(model_name=new_model_name,
                      make_id=new_make_id, body_style_id=new_body_style_id)

    return [dao, new_models]


@pytest.fixture
def new_dao() -> DBInterface:
    curr_dao = DBInterface(DB_URI)
    curr_dao.delete_all_users()
    curr_dao.delete_all_cities()
    curr_dao.delete_all_models()
    curr_dao.delete_all_makes()
    curr_dao.delete_all_watched_cars()
    curr_dao.delete_all_criteria()
    curr_dao.delete_all_watched_car_criteria()

    return curr_dao


def add_users(dao: DBInterface, users: list[dict]) -> list[DBInterface, list[dict]]:
    for user in users:
        dao.add_user(user)

    return [dao, users]


@pytest.fixture
def dao_with_users(new_dao: DBInterface, user_list: list) -> list[DBInterface, list]:

    return add_users(new_dao, user_list)


def add_cities(dao: DBInterface, cities: list[dict]):
    for city in cities:
        dao.add_city(city["city_name"])

    return [dao, cities]


@pytest.fixture
def dao_with_cities(new_dao: DBInterface, city_list: list[dict]) -> list[DBInterface, list]:
    return add_cities(new_dao, city_list)


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
    return add_makes(new_dao, make_list)


@pytest.fixture
def dao_with_body_styles(new_dao: DBInterface) -> DBInterface:
    new_dao = add_body_styles(new_dao)
    return new_dao


@pytest.fixture
def dao_with_web_body_styles(dao_with_body_styles: DBInterface) -> list[DBInterface, list[dict]]:
    dao_with_body_styles.delete_all_website_body_styles()
    web_body_styles = []
    for body_style in dao_with_body_styles.get_all_body_styles():
        for website in WEBSITE_NAMES:
            new_name = get_random_string(3, 10)
            dao_with_body_styles.add_website_body_style(
                body_style_id=body_style["id"], website_name=website, website_body_name=new_name)
            web_body_styles.append(
                {"website_name": website, "new_name": new_name, "body_style_id": body_style["id"]})

    return [dao_with_body_styles, web_body_styles]


@pytest.fixture
def dao_with_models(new_dao: DBInterface, make_list: list[dict]) -> list[DBInterface, list[dict], list[dict]]:
    new_dao = add_body_styles(new_dao)
    new_dao, make_list = add_makes(new_dao, make_list)
    new_dao, models_list = add_models(new_dao)

    return [new_dao, make_list, models_list]


def add_watched_cars(dao: DBInterface, watched_cars: list[dict]) -> list[DBInterface, list]:
    for car in watched_cars:
        dao.add_watched_car(
            vin=car["vin"], listing_url=car["listing_url"], last_price=car["last_price"])

    return [dao, watched_cars]


@pytest.fixture
def dao_with_watched_cars(new_dao: DBInterface, watched_car_list: list[dict]) -> list[DBInterface, list[dict]]:
    return add_watched_cars(new_dao, watched_car_list)


def criteria_list(body_styles: list[dict], cities: list[dict], models: list[dict], users: list[dict]) -> list[dict]:
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
        new_criteria["city_id"] = random.choice(cities)["id"]
        new_criteria["model_id"] = random.choice(models)["id"]
        new_criteria["body_style_id"] = random.choice(body_styles)["id"]

        criteria.append(new_criteria)

    return criteria


def add_criteria(dao: DBInterface, criteria_list: list[dict]) -> list[DBInterface, list[dict]]:
    for criteria in criteria_list:
        dao.add_criteria(
            min_year=criteria["min_year"],
            max_year=criteria["max_year"],
            min_price=criteria["min_price"],
            max_price=criteria["max_price"],
            max_mileage=criteria["max_mileage"],
            search_distance=criteria["search_distance"],
            no_accidents=criteria["no_accidents"],
            single_owner=criteria["single_owner"],
            user_id=criteria["user_id"],
            city_id=criteria["city_id"],
            model_id=criteria["model_id"],
            body_style_id=criteria["body_style_id"]
        )

    return [dao, criteria_list]


@pytest.fixture
def dao_with_criteria(new_dao: DBInterface, make_list: list[dict], city_list: list[dict], user_list: list[dict]) -> list[DBInterface, list[dict], list[dict], list[dict], list[dict], list[dict]]:
    new_dao, city_list = add_cities(new_dao, city_list)
    new_dao = add_body_styles(new_dao)
    new_dao, make_list = add_makes(new_dao, make_list)
    new_dao, models_list = add_models(new_dao)

    new_dao, user_list = add_users(new_dao, user_list)

    criteria = criteria_list(new_dao.get_all_body_styles(
    ), new_dao.get_all_cities(), new_dao.get_all_models(), new_dao.get_all_users())

    new_dao, criteria = add_criteria(new_dao, criteria)

    return [new_dao, city_list, criteria, make_list, models_list, user_list]


def add_watched_car_criteria(dao: DBInterface) -> list[DBInterface, list[dict], list[dict]]:
    watched_car_criteria = []
    criteria = dao.get_all_criteria()
    watched_cars = dao.get_all_watched_cars()
    pairs_seen = set()
    for _ in range(random.randint(5, 15)):
        new_row = {"criteria_id": random.choice(
            criteria)["id"], "watched_car_id": random.choice(watched_cars)["id"]}
        if (new_row["criteria_id"], new_row["watched_car_id"]) not in pairs_seen:
            dao.add_watched_car_criteria(**new_row)
            watched_car_criteria.append(new_row)
            pairs_seen.add((new_row["criteria_id"], new_row["watched_car_id"]))

    return [dao, watched_car_criteria]


@pytest.fixture
def dao_with_watched_car_criteria(dao_with_criteria: list[DBInterface, list[dict], list[dict], list[dict], list[dict], list[dict]], watched_car_list: list[dict]) -> list[DBInterface, list[dict], list[dict], list[dict], list[dict], list[dict], list[dict], list[dict]]:
    new_dao, city_list, criteria, make_list, models_list, user_list = dao_with_criteria

    new_dao, watched_cars = add_watched_cars(new_dao, watched_car_list)

    new_dao, watched_car_criteria = add_watched_car_criteria(new_dao)

    return [new_dao, city_list, criteria, make_list, models_list, user_list, watched_cars, watched_car_criteria]


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


def test_get_all_body_styles(dao_with_body_styles: DBInterface):
    res = dao_with_body_styles.get_all_body_styles()

    for res_body_style in res:
        assert res_body_style["body_style_name"] in body_styles


def test_get_specific_body_style(dao_with_body_styles: DBInterface):
    for style in body_styles:
        assert dao_with_body_styles.get_body_style_info(
            style)["body_style_name"] == style


def test_add_invalid_body_style(new_dao: DBInterface):
    with pytest.raises(psycopg.errors.InvalidTextRepresentation):
        new_dao.add_body_style("not a valid body style")


def test_get_all_web_body_styles(dao_with_web_body_styles: list[DBInterface, list[dict]]):
    dao, web_body_styles = dao_with_web_body_styles
    all_web_body_styles = dao.get_all_website_body_styles()

    assert len(all_web_body_styles) == len(body_styles) * len(WEBSITE_NAMES)

    web_body_style_names = set(
        web_body_style["new_name"] for web_body_style in web_body_styles)

    for style in all_web_body_styles:
        assert style["website_body_name"] in web_body_style_names


def test_get_specific_web_body_style(dao_with_web_body_styles: list[DBInterface, list[dict]]):
    dao, web_body_styles = dao_with_web_body_styles
    print(web_body_styles)

    for web_body_style in web_body_styles:
        retrieved_web_body_styles = dao.get_website_body_style_info(
            web_body_style["body_style_id"])

        assert len(retrieved_web_body_styles) == len(WEBSITE_NAMES)


def test_delete_specific_web_body_style(dao_with_web_body_styles: list[DBInterface, list[dict]]):
    dao, web_body_styles = dao_with_web_body_styles

    assert len(dao.get_all_website_body_styles()) == len(
        body_styles) * len(WEBSITE_NAMES)

    for web_body_style in web_body_styles:
        dao.delete_specific_website_body_style(web_body_style["body_style_id"])

    assert len(dao.get_all_website_body_styles()) == 0


def test_get_all_models(dao_with_models: list[DBInterface, list[dict], list[dict]]):
    dao, make_list, models_list = dao_with_models

    all_models_from_dao = dao.get_all_models()
    model_names_from_dao = {model["model_name"]
                            for model in all_models_from_dao}

    assert len(all_models_from_dao) == len(models_list)

    for model in models_list:
        assert model["model_name"] in model_names_from_dao


def test_get_model_by_make_id(dao_with_models: list[DBInterface, list[dict], list[dict]]):
    dao, make_list, models_list = dao_with_models

    models_by_make_id = defaultdict(list)

    for model in models_list:
        models_by_make_id[model["make_id"]].append(model)

    for make_id in models_by_make_id:
        dao_models_by_make_id = dao.get_models_by_make_id(make_id)
        assert len(dao_models_by_make_id) == len(models_by_make_id[make_id])

        for dao_model in dao_models_by_make_id:
            assert dao_model["make_id"] == make_id


def test_get_model_by_make_name(dao_with_models: list[DBInterface, list[dict], list[dict]]):
    dao, make_list, models_list = dao_with_models

    dao_make_info = dao.get_all_makes()

    models_by_make_id = defaultdict(list)

    for model in models_list:
        models_by_make_id[model["make_id"]].append(model)

    for make in dao_make_info:
        assert len(dao.get_model_by_make_name(make["make_name"])) == len(
            models_by_make_id[make["id"]])


def test_get_model_by_body_style_id(dao_with_models: list[DBInterface, list[dict], list[dict]]):
    dao, make_list, models_list = dao_with_models

    body_style_info = dao.get_all_body_styles()

    models_by_body_style = defaultdict(list)

    for model in models_list:
        models_by_body_style[model["body_style_id"]].append(model)

    for body_style in body_style_info:
        assert len(models_by_body_style[body_style["id"]]) == len(
            dao.get_model_by_body_style_id(body_style["id"]))


def test_get_model_by_body_style_name(dao_with_models: list[DBInterface, list[dict], list[dict]]):
    dao, make_list, models_list = dao_with_models

    body_style_info = dao.get_all_body_styles()
    models_by_body_style = defaultdict(list)

    for model in models_list:
        models_by_body_style[model["body_style_id"]].append(model)

    for body_style in body_style_info:
        assert len(models_by_body_style[body_style["id"]]) == len(
            dao.get_model_by_body_style_name(body_style["body_style_name"]))


def test_delete_model_by_model_name(dao_with_models: list[DBInterface, list[dict], list[dict]]):
    dao, make_list, models_list = dao_with_models

    print(models_list)
    print("\n")
    print(dao.get_all_models())

    assert len(dao.get_all_models()) > 0

    for model in models_list:
        dao.delete_model_by_model_name(model["model_name"])

    print("\n")
    print(dao.get_all_models())

    assert len(dao.get_all_models()) == 0


def test_get_all_watched_cars(dao_with_watched_cars: list[DBInterface, list[dict]]):
    dao, watched_cars = dao_with_watched_cars

    dao_watched_cars = dao.get_all_watched_cars()

    dao_watched_car_vins = {car["vin"] for car in dao_watched_cars}

    assert len(dao_watched_cars) == len(watched_cars)

    for car in watched_cars:
        assert car["vin"] in dao_watched_car_vins


def test_get_watched_car_by_vin(dao_with_watched_cars: list[DBInterface, list[dict]]):
    dao, watched_cars = dao_with_watched_cars

    for car in watched_cars:
        dao_car = dao.get_watched_car_by_vin(car["vin"])
        assert dao_car["vin"] == car["vin"]
        assert dao_car["listing_url"] == car["listing_url"]
        assert dao_car["last_price"] == car["last_price"]


def test_delete_watched_car_by_vin(dao_with_watched_cars: list[DBInterface, list[dict]]):
    dao, watched_cars = dao_with_watched_cars

    assert len(dao.get_all_watched_cars()) == len(watched_cars)

    for car in watched_cars:
        dao.delete_watched_car_by_vin(car["vin"])

    assert len(dao.get_all_watched_cars()) == 0


def test_get_all_criteria(dao_with_criteria: list[DBInterface, list[dict], list[dict], list[dict], list[dict], list[dict]]):
    dao, cities, criteria, makes, models, users = dao_with_criteria

    db_criteria = dao.get_all_criteria()
    assert len(db_criteria) == len(criteria)

    for crit in db_criteria:
        crit.pop("id")

    assert compare_data(criteria, db_criteria)


def test_get_criteria_by_info(dao_with_criteria: list[DBInterface, list[dict], list[dict], list[dict], list[dict], list[dict]]):
    dao, cities, criteria, makes, models, users = dao_with_criteria

    identical_criteria_count = defaultdict(int)

    for crit in criteria:
        identical_criteria_count[get_tuple_from_dict(crit)] += 1

    for crit in criteria:
        db_criteria = dao.get_criteria_by_info(**crit)[0]
        assert identical_criteria_count[get_tuple_from_dict(
            db_criteria)] == identical_criteria_count[get_tuple_from_dict(crit)]


def test_delete_criteria_by_info(dao_with_criteria: list[DBInterface, list[dict], list[dict], list[dict], list[dict], list[dict]]):
    dao, cities, criteria, makes, models, users = dao_with_criteria

    assert len(dao.get_all_criteria()) == len(criteria)

    for crit in criteria:
        dao.delete_criteria_by_info(**crit)

    assert len(dao.get_all_criteria()) == 0


def test_get_all_watched_car_criteria(dao_with_watched_car_criteria: list[DBInterface, list[dict], list[dict], list[dict], list[dict], list[dict], list[dict], list[dict]]):
    dao, city_list, criteria, make_list, models_list, user_list, watched_cars, watched_car_criteria = dao_with_watched_car_criteria

    db_data = dao.get_all_watched_car_criteria()
    assert len(db_data) == len(watched_car_criteria)

    assert compare_data(watched_car_criteria, db_data)


def test_get_watched_car_criteria_by_info(dao_with_watched_car_criteria: list[DBInterface, list[dict], list[dict], list[dict], list[dict], list[dict], list[dict], list[dict]]):
    dao, city_list, criteria, make_list, models_list, user_list, watched_cars, watched_car_criteria = dao_with_watched_car_criteria

    for crit in watched_car_criteria:
        assert compare_data(
            [crit], dao.get_watched_car_criteria_by_info(**crit))


def test_delete_watched_car_criteria_by_info(dao_with_watched_car_criteria: list[DBInterface, list[dict], list[dict], list[dict], list[dict], list[dict], list[dict], list[dict]]):
    dao, city_list, criteria, make_list, models_list, user_list, watched_cars, watched_car_criteria = dao_with_watched_car_criteria

    assert len(dao.get_all_watched_car_criteria()) == len(watched_car_criteria)

    for crit in watched_car_criteria:
        dao.delete_watched_car_criteria_by_info(**crit)

    assert len(dao.get_all_watched_car_criteria()) == 0
