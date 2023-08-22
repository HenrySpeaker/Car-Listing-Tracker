from tests.utils.db_utils import *
import pytest
from datacollection.find_cars import find_cars

TEST_CRITERIA_BASE = {"min_year": 1992, "max_year": 2023, "min_price": 100, "max_price": 1000000, "max_mileage": 150000, "search_distance": 50,
                      "no_accidents": True, "single_owner": False, "body_style_id": None}

TEST_ZIP = 90210
LISTING_DROP_CAR = {'vin': '2FAHP71V79X121646', 'listing_url': 'https://www.iseecars.com/view/listing?redirectUrl=https%3A%2F%2Fwww.carzing.com%2Fpartner%2Fvehicle%2F2FAHP71V79X121646%2FMTY0NjI5NTg%3D%3Futm_source%3Diseecars%26utm_medium%3Dreferral%26utm_campaign%3Dauto_finance%26utm_content%3Dsite%26utm_term%3D14l8Ejlm7XTuTuFK5bPSGD7D0IaIk4U_6s8iHgDG922GI9xdf5uQjkc6ojfgjaV5e&h=Z%2FBsCbBsAL7%2BAS%2BVIutE6gRBc4He1pJuXYcZENElMyoqNpFFy6C87aP4fW9Qk44USIc1wAQa1JcIuqdIeVBqfA%3D%3D&hh=y',
                    'last_price': 10000, 'model_year': 2009}


@pytest.fixture
def requests_mock(mocker):
    requests = mocker.MagicMock(name="requests")
    response = mocker.MagicMock(name="response")
    with open("tests/utils/isc_find_result.html", "r") as f:
        response.text = f.read()
    requests.get.return_value = response
    mocker.patch("datacollection.iseecars.requests", new=requests)
    return requests


@pytest.fixture
def dbi_with_isc_cv_criteria(dbi_with_users: list[DBInterface, list]) -> DBInterface:
    dbi, users = dbi_with_users
    model_id = dbi.get_model_by_name(model_name="Crown Victoria")["id"]
    user_id = dbi.get_all_users()[0]["id"]
    zip_code_id = dbi.get_zip_code_info(zip_code=TEST_ZIP)["id"]
    test_criteria = TEST_CRITERIA_BASE.copy()
    test_criteria["model_id"] = model_id
    test_criteria["user_id"] = user_id
    test_criteria["zip_code_id"] = zip_code_id
    dbi.add_criteria(**test_criteria)

    criteria_id = dbi.get_criteria_by_user_id(user_id=user_id)[0]["id"]
    price_drop_listing = LISTING_DROP_CAR.copy()
    price_drop_listing["criteria_id"] = criteria_id
    dbi.add_watched_car(**price_drop_listing)
    res = dbi.get_watched_car_by_vin(vin=price_drop_listing["vin"])
    dbi.add_alert(car_id=res["id"], change="new_listing")
    return dbi


@pytest.fixture
def dbi_with_isc_body_style_criteria(dbi_with_users: list[DBInterface, list]):
    dbi, users = dbi_with_users
    user_id = dbi.get_all_users()[0]["id"]
    zip_code_id = dbi.get_zip_code_info(zip_code=TEST_ZIP)["id"]
    body_style = "Convertible"
    body_style_id = dbi.get_body_style_info(body_style_name=body_style)["id"]
    test_criteria = TEST_CRITERIA_BASE.copy()
    test_criteria["user_id"] = user_id
    test_criteria["zip_code_id"] = zip_code_id
    test_criteria["model_id"] = None
    test_criteria["body_style_id"] = body_style_id
    dbi.add_criteria(**test_criteria)
    return dbi


def test_get_listings(requests_mock, dbi_with_isc_cv_criteria):
    find_cars()

    assert len(requests_mock.get.mock_calls) > 0
    assert len(dbi_with_isc_cv_criteria.get_all_alerts()) == 5


def test_no_response(requests_mock, dbi_with_isc_cv_criteria: DBInterface):
    requests_mock.get.return_value.text = ""
    find_cars()
    assert len(requests_mock.get.mock_calls) > 0

    # there will be one alert added automatically by the mocked fixture so no others should be added
    assert len(dbi_with_isc_cv_criteria.get_all_alerts()) == 1


def test_get_listings_body_style_criteria(requests_mock, dbi_with_isc_body_style_criteria):
    find_cars()
    assert len(requests_mock.get.mock_calls) > 0
    assert len(dbi_with_isc_body_style_criteria.get_all_alerts()) == 5


def test_price_drop_no_alerts(requests_mock, dbi_with_isc_cv_criteria):
    dbi = dbi_with_isc_cv_criteria
    dbi.delete_all_alerts()
    find_cars()
    assert len(requests_mock.get.mock_calls) > 0
    assert len(dbi_with_isc_cv_criteria.get_all_alerts()) == 5
