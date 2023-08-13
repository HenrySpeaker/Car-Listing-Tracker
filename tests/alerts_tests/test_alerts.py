import pytest
# import alerts.alerts as alerts
# from tests.utils.db_utils import *


# @pytest.fixture
# def mocked_smtp(mocker):
#     mock_SMTP = mocker.MagicMock(name="alerts.smtplib.SMTP")
#     mocker.patch("alerts.smtplib.SMTP", new=mock_SMTP)


# def test_alerts(mocked_smtp, dao_with_listing_alerts: list[DBInterface, list[dict], list[dict], list[dict]]):
#     dao, users, watched_cars, alerts = dao_with_listing_alerts
