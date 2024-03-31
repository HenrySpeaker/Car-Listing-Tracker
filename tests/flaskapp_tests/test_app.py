from random import choice
from bs4 import BeautifulSoup
import pytest
from werkzeug.security import generate_password_hash, check_password_hash
from flaskapp import create_app
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from config import DevConfig
from db.dbi.db_interface import DBInterface


DB_URI = DevConfig.POSTGRES_DATABASE_URI

# Fake user data
FAKE_USER = "FAKE USERNAME"
FAKE_EMAIL = "FAKE@EMAIL.com"
FAKE_PASSWORD = "FAKEPASSWORD"
FAKE_FREQ = 5

TEST_CRITERIA = {"min_year": 1992, "max_year": 2023, "min_price": 100, "max_price": 1000000, "max_mileage": 150000,
                 "search_distance": 35, "no_accidents": True, "single_owner": False}


def add_fake_user_to_db():
    dbi = DBInterface(DB_URI)

    if not dbi.get_user_by_username(FAKE_USER):
        dbi.add_user({
            "username": FAKE_USER,
            "email": FAKE_EMAIL,
            "password_hash": generate_password_hash(FAKE_PASSWORD),
            "notification_frequency": FAKE_FREQ
        })


@pytest.fixture
def selenium_driver():
    # Ensures that the webdriver is closed after the test
    driver = webdriver.Firefox()
    yield driver
    driver.close()


def test_home_page():
    """
    GIVEN a flask app configured for testing
    WHEN the '/' page is requested
    THEN check that the response is valid
    """

    app = create_app(DevConfig)

    with app.test_client() as test_client:
        response = test_client.get("/")

        assert response.status_code == 200


def test_nonexistent_page():
    """
    GIVEN a flask app configured for testing
    WHEN the '/not-a-page' page is requested
    THEN check that the response is invalid
    """

    app = create_app(DevConfig)

    with app.test_client() as test_client:
        response = test_client.get("/not-a-page")

        assert response.status_code == 404


def test_register_page_with_selenium(flask_port, selenium_driver):
    """
    GIVEN a flask app configured for testing
    WHEN the register page is accessed
    THEN check that the page loads correctly and the user data submitted is added to the database
    """

    dbi = DBInterface(DB_URI)

    url = f"http://localhost:{flask_port}/register"
    selenium_driver.get(url)
    assert "Register" in selenium_driver.title

    if dbi.get_user_by_username(FAKE_USER) or dbi.get_user_by_email(FAKE_EMAIL):
        dbi.delete_user_by_username(FAKE_USER)

    assert dbi.get_user_by_username(FAKE_USER) == None
    assert dbi.get_user_by_email(FAKE_EMAIL) == None

    username_element = selenium_driver.find_element(By.NAME, "username")
    username_element.send_keys(FAKE_USER)

    email_element = selenium_driver.find_element(By.NAME, "email")
    email_element.send_keys(FAKE_EMAIL)

    password_element = selenium_driver.find_element(By.NAME, "password")
    password_element.send_keys(FAKE_PASSWORD)

    frequency_element = selenium_driver.find_element(
        By.NAME, "notification_frequency")
    frequency_element.send_keys(FAKE_FREQ)

    selenium_driver.find_element(By.ID, "submit").click()

    assert dbi.get_user_by_username(FAKE_USER) != None
    assert dbi.get_user_by_email(FAKE_EMAIL) != None

    assert selenium_driver.current_url == f"http://localhost:{flask_port}/login"


def test_login_page_with_email_with_selenium(flask_port, selenium_driver):
    """
    GIVEN a flask app configured for testing
    WHEN the login page is accessed and a valid email and password are submitted
    THEN check that the user is logged in and redirected to the account page
    """

    dbi = DBInterface(DB_URI)

    url = f"http://localhost:{flask_port}/login"
    selenium_driver.get(url)

    add_fake_user_to_db()

    assert "Login" in selenium_driver.title

    email_element = selenium_driver.find_element(By.NAME, "email")
    email_element.send_keys(FAKE_EMAIL)

    password_element = selenium_driver.find_element(By.NAME, "password")
    password_element.send_keys(FAKE_PASSWORD)

    selenium_driver.find_element(By.ID, "submit").click()

    assert selenium_driver.current_url == f"http://localhost:{flask_port}/account"


def login_user(flask_port, selenium_driver):
    dbi = DBInterface(DB_URI)

    url = f"http://localhost:{flask_port}/login"
    selenium_driver.get(url)

    add_fake_user_to_db()

    assert "Login" in selenium_driver.title

    username_element = selenium_driver.find_element(By.NAME, "username")
    username_element.send_keys(FAKE_USER)

    password_element = selenium_driver.find_element(By.NAME, "password")
    password_element.send_keys(FAKE_PASSWORD)

    selenium_driver.find_element(By.ID, "submit").click()

    return selenium_driver


def test_login_page_with_username_with_selenium(flask_port, selenium_driver):
    """
    GIVEN a flask app configured for testing
    WHEN the login page is accessed and a valid username and password are submitted
    THEN check that the user is logged in and redirected to the account page
    """

    dbi = DBInterface(DB_URI)

    url = f"http://localhost:{flask_port}/login"
    selenium_driver.get(url)

    add_fake_user_to_db()

    selenium_driver = login_user(flask_port, selenium_driver)

    assert selenium_driver.current_url == f"http://localhost:{flask_port}/account"


def test_login_page_with_invalid_credentials_with_selenium(flask_port, selenium_driver):
    """
    GIVEN a flask app configured for testing
    WHEN the login page is accessed and invalid credentials are submitted
    THEN check that the page is sent back to /login
    """

    dbi = DBInterface(DB_URI)

    url = f"http://localhost:{flask_port}/login"
    selenium_driver.get(url)

    add_fake_user_to_db()

    assert "Login" in selenium_driver.title

    username_element = selenium_driver.find_element(By.NAME, "username")
    username_element.send_keys(FAKE_USER)

    password_element = selenium_driver.find_element(By.NAME, "password")
    password_element.send_keys("WRONG Password")

    selenium_driver.find_element(By.ID, "submit").click()

    assert selenium_driver.current_url == f"http://localhost:{flask_port}/login"


def test_logout_with_selenium(flask_port, selenium_driver):
    """
    GIVEN a flask app configured for testing
    WHEN the logout link is clicked
    THEN check that the user is logged out and redirected to the home page
    """

    dbi = DBInterface(DB_URI)

    url = f"http://localhost:{flask_port}/login"
    selenium_driver.get(url)

    add_fake_user_to_db()

    selenium_driver = login_user(flask_port, selenium_driver)

    assert selenium_driver.current_url == f"http://localhost:{flask_port}/account"

    # WebDriverWait(selenium_driver, 20).until(EC.element_to_be_clickable((By.ID, "logout"))).click()

    selenium_driver.find_element(By.ID, "logout").find_element(By.XPATH, "*").click()

    assert selenium_driver.current_url == f"http://localhost:{flask_port}/login"


def go_to_add_criteria(selenium_driver, flask_port):
    selenium_driver = login_user(flask_port, selenium_driver)

    selenium_driver.find_element(
        By.ID, "add-criteria").find_element(By.XPATH, "*").click()

    return selenium_driver


def test_add_criteria_page_with_selenium(flask_port, selenium_driver):
    """
    GIVEN a flask app configured for testing
    WHEN the login page is accessed, valid credentials are submitted, and then the /add-criteria page is accessed
    THEN check that the page loads and the links are provided
    """

    dbi = DBInterface(DB_URI)

    url = f"http://localhost:{flask_port}/login"
    selenium_driver.get(url)

    add_fake_user_to_db()

    selenium_driver = go_to_add_criteria(selenium_driver, flask_port)

    body_style_link = selenium_driver.find_element(By.ID, "add-body-style")
    href_val = "/add-criteria/body-style"
    assert body_style_link.get_attribute("href")[-len(href_val):] == href_val

    make_elements = selenium_driver.find_elements(By.CLASS_NAME, "make-opt")

    makes_list = dbi.get_all_makes()

    assert len(make_elements) == len(makes_list)

    for elem in make_elements:
        assert dbi.get_make_info(elem.get_attribute("id")) != None


def add_criteria(selenium_driver, test_criteria):
    dbi = DBInterface(DB_URI)

    if dbi.get_criteria_by_info(**test_criteria):
        dbi.delete_criteria_by_info(**test_criteria)

    assert dbi.get_criteria_by_info(**test_criteria) == []

    min_year_element = selenium_driver.find_element(By.ID, "min_year")
    min_year_element.send_keys(test_criteria["min_year"])
    max_year_element = selenium_driver.find_element(By.ID, "max_year")
    max_year_element.send_keys(test_criteria["max_year"])

    min_price_element = selenium_driver.find_element(By.ID, "min_price")
    min_price_element.send_keys(str(test_criteria["min_price"])[:-1])
    max_price_element = selenium_driver.find_element(By.ID, "max_price")
    max_price_element.send_keys(test_criteria["max_price"])

    max_mileage_element = selenium_driver.find_element(By.ID, "max_mileage")
    max_mileage_element.send_keys(test_criteria["max_mileage"])

    search_distance_element = selenium_driver.find_element(
        By.ID, "search_distance")
    search_distance_element.clear()
    search_distance_element.send_keys(test_criteria["search_distance"])

    no_accidents_element = selenium_driver.find_element(By.ID, "no_accidents")
    if test_criteria["no_accidents"]:
        no_accidents_element.click()

    single_owner_element = selenium_driver.find_element(By.ID, "single_owner")
    if test_criteria["single_owner"]:
        single_owner_element.click()

    zip_code_element = selenium_driver.find_element(By.ID, "zip_code")
    zip_code_element.send_keys("90210")

    return selenium_driver


def test_add_body_style_criteria_with_selenium(flask_port, selenium_driver):
    """
    GIVEN a flask app configured for testing
    WHEN the /add-criteria page is accessed
    THEN check that the the body style criteria page can be accessed and a search is submitted successfully
    """

    dbi = DBInterface(DB_URI)

    url = f"http://localhost:{flask_port}/login"
    selenium_driver.get(url)

    add_fake_user_to_db()

    selenium_driver = go_to_add_criteria(selenium_driver, flask_port)

    selenium_driver.find_element(By.ID, "add-body-style").click()

    assert selenium_driver.current_url == f"http://localhost:{flask_port}/add-criteria/body-style"

    selenium_driver = add_criteria(selenium_driver, TEST_CRITERIA)

    body_style_element = Select(
        selenium_driver.find_element(By.ID, "body_style"))
    body_style = "Sedan"
    body_style_element.select_by_visible_text(body_style)

    selenium_driver.find_element(By.ID, "submit").click()

    criteria_response = dbi.get_all_criteria()[0]

    print(DB_URI)
    print(criteria_response)

    for key in TEST_CRITERIA:
        assert TEST_CRITERIA[key] == criteria_response[key]

    assert criteria_response["body_style_id"] == dbi.get_body_style_info(body_style)[
        "id"]


def add_make_model_criteria(selenium_driver, dbi):
    all_makes = dbi.get_all_makes()
    curr_make = choice(all_makes)["make_name"]

    curr_model = choice(dbi.get_model_by_make_name(curr_make))["model_name"]

    selenium_driver.find_element(By.ID, curr_make).click()

    selenium_driver.find_element(By.ID, "submit").click()

    selenium_driver = add_criteria(selenium_driver, TEST_CRITERIA)

    model_element = Select(selenium_driver.find_element(By.ID, "model_name"))

    model_element.select_by_visible_text(curr_model)

    selenium_driver.find_element(By.ID, "submit").click()

    return selenium_driver, curr_make, curr_model


def test_add_make_model_criteria_with_selenium(flask_port, selenium_driver):
    """
    GIVEN a flask app configured for testing
    WHEN the /add-criteria page is accessed
    THEN check that the the make-model criteria page can be accessed and a search is submitted successfully
    """

    dbi = DBInterface(DB_URI)

    url = f"http://localhost:{flask_port}/login"
    selenium_driver.get(url)

    add_fake_user_to_db()

    selenium_driver = go_to_add_criteria(selenium_driver, flask_port)

    selenium_driver, curr_make, curr_model = add_make_model_criteria(
        selenium_driver, dbi)

    criteria_response = dbi.get_all_criteria()[0]

    for key in TEST_CRITERIA:
        assert TEST_CRITERIA[key] == criteria_response[key]

    assert criteria_response["model_id"] == dbi.get_model_by_name(curr_model)[
        "id"]


def test_criteria_page_with_selenium(flask_port, selenium_driver):
    """
    GIVEN a flask app configured for testing
    WHEN search criteria is added and the /criteria page is accessed
    THEN check that the the search criteria submitted matches the search criteria displayed
    """

    dbi = DBInterface(DB_URI)

    url = f"http://localhost:{flask_port}/login"
    selenium_driver.get(url)

    add_fake_user_to_db()

    selenium_driver = go_to_add_criteria(selenium_driver, flask_port)

    selenium_driver, curr_make, curr_model = add_make_model_criteria(
        selenium_driver, dbi)

    html = selenium_driver.page_source

    check_criteria_page_for_db_match(html)


def test_account_page_not_logged_in():
    """
    GIVEN a flask app configured for testing
    WHEN the '/account' page is requested without being logged in
    THEN check that the response is 401
    """

    app = create_app(DevConfig)

    with app.test_client() as test_client:
        response = test_client.get("/account")

        assert response.status_code == 401


def test_criteria_page_not_logged_in():
    """
    GIVEN a flask app configured for testing
    WHEN the '/criteria' page is requested without being logged in
    THEN check that the response is 401
    """

    app = create_app(DevConfig)

    with app.test_client() as test_client:
        response = test_client.get("/criteria")

        assert response.status_code == 401


def test_add_criteria_page_not_logged_in():
    """
    GIVEN a flask app configured for testing
    WHEN the '/add-criteria' page is requested without being logged in
    THEN check that the response is 401
    """

    app = create_app(DevConfig)

    with app.test_client() as test_client:
        response = test_client.get("/add-criteria")

        assert response.status_code == 401


def test_add_criteria_body_style_page_not_logged_in():
    """
    GIVEN a flask app configured for testing
    WHEN the '/add-criteria' page is requested without being logged in
    THEN check that the response is 401
    """

    app = create_app(DevConfig)

    with app.test_client() as test_client:
        response = test_client.get("/add-criteria/body-style")

        assert response.status_code == 401


def test_add_criteria_make_model_not_logged_in():
    """
    GIVEN a flask app configured for testing
    WHEN the '/add-criteria' page is requested without being logged in
    THEN check that the response is 401
    """

    app = create_app(DevConfig)

    with app.test_client() as test_client:
        response = test_client.get("/add-criteria/Honda")

        assert response.status_code == 401


def test_login_page():
    """
    GIVEN a flask app configured for testing
    WHEN the '/login' page is requested
    THEN check that the response is 200
    """

    app = create_app(DevConfig)

    with app.test_client() as test_client:
        response = test_client.get("/login")

        assert response.status_code == 200


def test_login_page_form_submit_with_username():
    """
    GIVEN a flask app configured for testing
    WHEN the '/login' page is requested, a user is in the database, and a valid login form is submitted with username
    THEN check that the response is 200
    """

    app = create_app(DevConfig)

    add_fake_user_to_db()

    data = {
        "username": FAKE_USER,
        "email": "",
        "password": FAKE_PASSWORD
    }

    dbi = DBInterface(DB_URI)

    assert check_password_hash(dbi.get_user_by_username(FAKE_USER)[
                               "password_hash"], FAKE_PASSWORD)

    with app.test_client() as test_client:
        with app.app_context():
            app.config['WTF_CSRF_ENABLED'] = False
            response = test_client.post(
                "/login", data=data, follow_redirects=True)

            assert response.status_code == 200


def test_login_page_form_submit_with_username_and_invalid_password():
    """
    GIVEN a flask app configured for testing
    WHEN the '/login' page is requested, a user is in the database, and a login form is submitted with username and incorrect password
    THEN check that the response is 302
    """

    app = create_app(DevConfig)

    add_fake_user_to_db()

    data = {
        "username": FAKE_USER,
        "email": "",
        "password": "WRONG PASSWORD"
    }

    dbi = DBInterface(DB_URI)

    assert check_password_hash(dbi.get_user_by_username(FAKE_USER)[
                               "password_hash"], FAKE_PASSWORD)

    with app.test_client() as test_client:
        with app.app_context():
            app.config['WTF_CSRF_ENABLED'] = False
            response = test_client.post(
                "/login", data=data, follow_redirects=False)

            assert response.status_code == 302


def test_login_page_form_submit_with_email():
    """
    GIVEN a flask app configured for testing
    WHEN the '/login' page is requested, a user is in the database, and a valid login form is submitted with email
    THEN check that the response is 200
    """

    app = create_app(DevConfig)

    add_fake_user_to_db()

    data = {
        "username": "",
        "email": FAKE_EMAIL,
        "password": FAKE_PASSWORD
    }

    dbi = DBInterface(DB_URI)

    assert check_password_hash(dbi.get_user_by_email(FAKE_EMAIL)[
                               "password_hash"], FAKE_PASSWORD)

    with app.test_client() as test_client:
        with app.app_context():
            app.config['WTF_CSRF_ENABLED'] = False
            response = test_client.post(
                "/login", data=data, follow_redirects=True)

            assert response.status_code == 200


def test_login_page_form_submit_with_email_and_invalid_password():
    """
    GIVEN a flask app configured for testing
    WHEN the '/login' page is requested, a user is in the database, and a login form is submitted with email and incorrect password
    THEN check that the response is 302
    """

    app = create_app(DevConfig)

    add_fake_user_to_db()

    data = {
        "username": "",
        "email": FAKE_EMAIL,
        "password": "WRONG PASSWORD"
    }

    dbi = DBInterface(DB_URI)

    assert check_password_hash(dbi.get_user_by_username(FAKE_USER)[
                               "password_hash"], FAKE_PASSWORD)

    with app.test_client() as test_client:
        with app.app_context():
            app.config['WTF_CSRF_ENABLED'] = False
            response = test_client.post(
                "/login", data=data, follow_redirects=False)

            assert response.status_code == 302


def test_login_page_form_submit_with_both_username_and_email():
    """
    GIVEN a flask app configured for testing
    WHEN the '/login' page is requested, a user is in the database, and a login form is submitted with username, email, and password
    THEN check that the user is redirected back to the login page and an error response is given
    """

    app = create_app(DevConfig)

    add_fake_user_to_db()

    data = {
        "username": FAKE_USER,
        "email": FAKE_EMAIL,
        "password": FAKE_PASSWORD
    }

    dbi = DBInterface(DB_URI)

    assert check_password_hash(dbi.get_user_by_username(FAKE_USER)[
                               "password_hash"], FAKE_PASSWORD)

    with app.test_client() as test_client:
        with app.app_context():
            app.config['WTF_CSRF_ENABLED'] = False
            response = test_client.post(
                "/login", data=data, follow_redirects=True)

            assert b"Only one of email or password can be submitted." in response.data


def test_login_page_form_submit_with_short_username():
    """
    GIVEN a flask app configured for testing
    WHEN the '/login' page is requested, a user is in the database, and a login form is submitted with a short username and password
    THEN check that the user is redirected back to the login page and an error response is given
    """

    app = create_app(DevConfig)

    add_fake_user_to_db()

    data = {
        "username": "A",
        "email": "",
        "password": FAKE_PASSWORD
    }

    dbi = DBInterface(DB_URI)

    assert check_password_hash(dbi.get_user_by_username(FAKE_USER)[
                               "password_hash"], FAKE_PASSWORD)

    with app.test_client() as test_client:
        with app.app_context():
            app.config['WTF_CSRF_ENABLED'] = False
            response = test_client.post(
                "/login", data=data, follow_redirects=True)

            soup = BeautifulSoup(response.data, "html.parser")

            # checks that user is directed back to login page because of invalid username
            assert soup.find("input", value="Login") != None


def test_register_page():
    """
    GIVEN a flask app configured for testing
    WHEN the '/register' page is requested
    THEN check that the response is 200
    """

    app = create_app(DevConfig)

    with app.test_client() as test_client:
        response = test_client.get("/register")

        assert response.status_code == 200


def test_register_page_form_submit():
    """
    GIVEN a flask app configured for testing
    WHEN the '/register' page is requested, a user is in the database, and a valid register form is submitted
    THEN check that the user information is added to the database
    """

    app = create_app(DevConfig)

    data = {
        "username": FAKE_USER,
        "email": FAKE_EMAIL,
        "password": FAKE_PASSWORD,
        "notification_frequency": 3
    }

    dbi = DBInterface(DB_URI)

    if dbi.get_user_by_email(data["email"]) or dbi.get_user_by_username(data["username"]):
        dbi.delete_user_by_username(data["username"])

    assert dbi.get_user_by_username(data["username"]) == None
    assert dbi.get_user_by_email(data["email"]) == None

    with app.test_client() as test_client:
        with app.app_context():
            app.config['WTF_CSRF_ENABLED'] = False
            response = test_client.post(
                "/register", data=data, follow_redirects=True)

            assert response.status_code == 200

    db_result = dbi.get_user_by_username(data["username"])

    assert db_result["email"] == data["email"]
    assert db_result["username"] == data["username"]
    assert db_result["notification_frequency"] == data["notification_frequency"]


def test_criteria_page(flask_port, selenium_driver):
    """
    GIVEN a flask app configured for testing with a search criteria added to the account
    WHEN the '/criteria' page is requested
    THEN check that the search criteria information is displayed on the page
    """

    url = f"http://localhost:{flask_port}/login"
    selenium_driver.get(url)

    add_fake_user_to_db()

    selenium_driver = go_to_add_criteria(selenium_driver, flask_port)

    selenium_driver.find_element(By.ID, "add-body-style").click()

    selenium_driver = add_criteria(selenium_driver, TEST_CRITERIA)

    body_style_element = Select(
        selenium_driver.find_element(By.ID, "body_style"))
    body_style = "Sedan"
    body_style_element.select_by_visible_text(body_style)

    selenium_driver.find_element(By.ID, "submit").click()

    app = create_app(DevConfig)

    data = {
        "username": FAKE_USER,
        "email": "",
        "password": FAKE_PASSWORD
    }

    dbi = DBInterface(DB_URI)

    assert dbi.get_all_criteria() != []

    with app.test_client() as test_client:
        with app.app_context():
            app.config['WTF_CSRF_ENABLED'] = False
            response = test_client.post(
                "/login", data=data, follow_redirects=True)

            assert response.status_code == 200

            criteria_response = test_client.get("/criteria")

            check_criteria_page_for_db_match(criteria_response.data)


def check_criteria_page_for_db_match(html):
    dbi = DBInterface(DB_URI)
    soup = BeautifulSoup(html, "html.parser")

    data = []

    for tr in soup.find('table').find_all('tr'):
        row = {td.get('id'): td.text for td in tr.find_all('td')
               if td.get('id') not in ("view-cars", "remove-criteria", "start-search", "send-new-alerts")}

        # avoids including the header row since there are no tr elements
        if row == {}:
            continue

        data.append(row)

    db_data = dbi.get_all_criteria()

    assert len(data) == len(db_data)

    for criteria in data:
        assert dbi.get_criteria_by_info(
            **{key: criteria[key] for key in criteria if key not in ("make_name", "model_name", "body_style_name", "send-car-alerts")}) != []


def test_add_criteria_page():
    """
    GIVEN a flask app configured for testing
    WHEN the '/add-criteria' page is requested
    THEN check that the appropriate criteria links are provided
    """
    dbi = DBInterface(DB_URI)

    all_makes = [make["make_name"] for make in dbi.get_all_makes()]
    all_makes.sort()

    app = create_app(DevConfig)

    data = {
        "username": FAKE_USER,
        "email": "",
        "password": FAKE_PASSWORD
    }

    add_fake_user_to_db()

    with app.test_client() as test_client:
        with app.app_context():
            app.config['WTF_CSRF_ENABLED'] = False
            response = test_client.post(
                "/login", data=data, follow_redirects=True)

            assert response.status_code == 200

            criteria_response = test_client.get("/add-criteria")

            soup = BeautifulSoup(criteria_response.data, "html.parser")

            page_makes = [opt.get("value")
                          for opt in soup.find_all("option", class_="make-opt")]

            page_makes.sort()
            print(page_makes)

            assert len(all_makes) == len(page_makes)

            assert all_makes == page_makes


def test_add_criteria_body_style():
    """
    GIVEN a flask app configured for testing
    WHEN the '/add-criteria/body-style' page is requested, and a valid body style criteria form is submitted
    THEN check that the criteria information is added to the database
    """
    dbi = DBInterface(DB_URI)

    app = create_app(DevConfig)

    data = {
        "username": FAKE_USER,
        "email": "",
        "password": FAKE_PASSWORD
    }

    add_fake_user_to_db()
    user_id = dbi.get_user_by_username(username=data["username"])["id"]

    # if dbi.get_criteria_by_info(**TEST_CRITERIA):
    #     dbi.delete_criteria_by_info(**TEST_CRITERIA)

    if dbi.get_all_criteria():
        dbi.delete_all_criteria()

    assert dbi.get_criteria_by_info(**TEST_CRITERIA) == []

    form_data = TEST_CRITERIA.copy()
    body_style = "Convertible"
    form_data["body_style"] = body_style
    form_data["zip_code"] = 90210

    with app.test_client() as test_client:
        with app.app_context():
            app.config['WTF_CSRF_ENABLED'] = False
            login_response = test_client.post(
                "/login", data=data, follow_redirects=True)

            assert login_response.status_code == 200

            page_response = test_client.get('/add-criteria/body-style')

            assert page_response.status_code == 200

            add_response = test_client.post(
                '/add-criteria/body-style', data=form_data, follow_redirects=True)

            assert add_response.status_code == 200

            db_response = dbi.get_criteria_by_user_id(user_id=user_id)
            assert len(db_response) == 1

            assert db_response[0]["body_style_id"] == dbi.get_body_style_info(body_style)[
                "id"]


def test_add_criteria_make_model():
    """
    GIVEN a flask app configured for testing
    WHEN the '/add-criteria/<make>' page is requested, and a valid make and model criteria form is submitted
    THEN check that the criteria information is added to the database
    """
    dbi = DBInterface(DB_URI)

    app = create_app(DevConfig)

    data = {
        "username": FAKE_USER,
        "email": "",
        "password": FAKE_PASSWORD
    }

    add_fake_user_to_db()
    user_id = dbi.get_user_by_username(username=data["username"])["id"]

    # if dbi.get_criteria_by_info(**TEST_CRITERIA):
    #     dbi.delete_criteria_by_info(**TEST_CRITERIA)

    if dbi.get_all_criteria():
        dbi.delete_all_criteria()

    assert dbi.get_criteria_by_info(**TEST_CRITERIA) == []

    form_data = TEST_CRITERIA.copy()
    model_name = "Vantage"
    form_data["model_name"] = model_name
    form_data["zip_code"] = 90210

    with app.test_client() as test_client:
        with app.app_context():
            app.config['WTF_CSRF_ENABLED'] = False
            login_response = test_client.post(
                "/login", data=data, follow_redirects=True)

            assert login_response.status_code == 200

            page_response = test_client.get('/add-criteria/Aston%20Martin')

            assert page_response.status_code == 200

            add_response = test_client.post(
                '/add-criteria/Aston%20Martin', data=form_data, follow_redirects=True)

            assert add_response.status_code == 200

            db_response = dbi.get_criteria_by_user_id(user_id=user_id)
            assert len(db_response) == 1

            assert db_response[0]["model_id"] == dbi.get_model_by_name(model_name)[
                "id"]


def test_add_criteria_invalid_years():
    """
    GIVEN a flask app configured for testing
    WHEN the '/add-criteria/body-style' page is requested, and a body style criteria form is submitted with min_year > max_year
    THEN check that the criteria information is not added to the database and an error message is shown
    """
    dbi = DBInterface(DB_URI)

    app = create_app(DevConfig)

    data = {
        "username": FAKE_USER,
        "email": "",
        "password": FAKE_PASSWORD
    }

    add_fake_user_to_db()

    if dbi.get_criteria_by_info(**TEST_CRITERIA):
        dbi.delete_criteria_by_info(**TEST_CRITERIA)

    assert dbi.get_criteria_by_info(**TEST_CRITERIA) == []

    form_data = TEST_CRITERIA.copy()
    body_style = "Convertible"
    form_data["body_style"] = body_style
    form_data["zip_code"] = 90210
    form_data["min_year"] = 2020
    form_data["max_year"] = 2019

    with app.test_client() as test_client:
        with app.app_context():
            app.config['WTF_CSRF_ENABLED'] = False
            login_response = test_client.post(
                "/login", data=data, follow_redirects=True)

            assert login_response.status_code == 200

            page_response = test_client.get('/add-criteria/body-style')

            assert page_response.status_code == 200

            add_response = test_client.post(
                '/add-criteria/body-style', data=form_data, follow_redirects=True)

            assert add_response.status_code == 200

            db_response = dbi.get_criteria_by_info(**TEST_CRITERIA)
            assert len(db_response) == 0

            assert b"Minimum year must be less than maximum year" in add_response.data


def test_add_criteria_invalid_prices():
    """
    GIVEN a flask app configured for testing
    WHEN the '/add-criteria/body-style' page is requested, and a body style criteria form is submitted with min_price > max_price
    THEN check that the criteria information is not added to the database and an error message is shown
    """
    dbi = DBInterface(DB_URI)

    app = create_app(DevConfig)

    data = {
        "username": FAKE_USER,
        "email": "",
        "password": FAKE_PASSWORD
    }

    add_fake_user_to_db()

    if dbi.get_criteria_by_info(**TEST_CRITERIA):
        dbi.delete_criteria_by_info(**TEST_CRITERIA)

    assert dbi.get_criteria_by_info(**TEST_CRITERIA) == []

    form_data = TEST_CRITERIA.copy()
    body_style = "Convertible"
    form_data["body_style"] = body_style
    form_data["zip_code"] = 90210
    form_data["max_price"] = 1

    with app.test_client() as test_client:
        with app.app_context():
            app.config['WTF_CSRF_ENABLED'] = False
            login_response = test_client.post(
                "/login", data=data, follow_redirects=True)

            assert login_response.status_code == 200

            page_response = test_client.get('/add-criteria/body-style')

            assert page_response.status_code == 200

            add_response = test_client.post(
                '/add-criteria/body-style', data=form_data, follow_redirects=True)

            assert add_response.status_code == 200

            db_response = dbi.get_criteria_by_info(**TEST_CRITERIA)
            assert len(db_response) == 0

            assert b"Minimum car price must be less than maximum car price" in add_response.data


def test_add_criteria_invalid_zip_code():
    """
    GIVEN a flask app configured for testing
    WHEN the '/add-criteria/body-style' page is requested, and a body style criteria form is submitted with an invalid zip code
    THEN check that the criteria information is not added to the database and an error message is shown
    """
    dbi = DBInterface(DB_URI)

    app = create_app(DevConfig)

    data = {
        "username": FAKE_USER,
        "email": "",
        "password": FAKE_PASSWORD
    }

    add_fake_user_to_db()

    if dbi.get_criteria_by_info(**TEST_CRITERIA):
        dbi.delete_criteria_by_info(**TEST_CRITERIA)

    assert dbi.get_criteria_by_info(**TEST_CRITERIA) == []

    form_data = TEST_CRITERIA.copy()
    body_style = "Convertible"
    form_data["body_style"] = body_style
    form_data["zip_code"] = 1

    with app.test_client() as test_client:
        with app.app_context():
            app.config['WTF_CSRF_ENABLED'] = False
            login_response = test_client.post(
                "/login", data=data, follow_redirects=True)

            assert login_response.status_code == 200

            page_response = test_client.get('/add-criteria/body-style')

            assert page_response.status_code == 200

            add_response = test_client.post(
                '/add-criteria/body-style', data=form_data, follow_redirects=True)

            assert add_response.status_code == 200

            db_response = dbi.get_criteria_by_info(**TEST_CRITERIA)
            assert len(db_response) == 0

            assert b"Must enter a valid zip code." in add_response.data
