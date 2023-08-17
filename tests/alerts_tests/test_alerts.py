import pytest
import useralerts.alerts as alerts
from tests.utils.db_utils import *
import smtplib
from datetime import datetime, timedelta


@pytest.fixture
def mocked_smtp(mocker):
    mock_SMTP = mocker.MagicMock(name="alerts.smtplib.SMTP")
    mocker.patch("useralerts.alerts.smtplib.SMTP", new=mock_SMTP)
    return mock_SMTP


@pytest.fixture
def dao_with_adjusted_last_alerted(dao_with_listing_alerts: list[DBInterface, list[dict], list[dict], list[dict]]):
    dao, users, watched_cars, alerts_list = dao_with_listing_alerts

    # ensure that all users will get alerted by moving the last_alerted time earlier
    user_list = dao.get_all_users()
    for user in user_list:
        dao.update_last_alerted_by_id(
            user["id"], datetime.now() - timedelta(days=100))

    return dao


def test_alerts(mocked_smtp, dao_with_adjusted_last_alerted):
    dao = dao_with_adjusted_last_alerted

    assert len(dao.get_all_alerts()) > 0
    alerts.send_alerts()
    mocked_smtp.return_value.__enter__.return_value.starttls.assert_called()
    mocked_smtp.return_value.__enter__.return_value.login.assert_called()
    mocked_smtp.return_value.__enter__.return_value.sendmail.assert_called()


def test_alerts_not_sent_early(mocked_smtp, dao_with_listing_alerts: list[DBInterface, list[dict], list[dict], list[dict]]):

    alerts.send_alerts()
    assert mocked_smtp.return_value.__enter__.return_value.starttls.call_count == 0
    assert mocked_smtp.return_value.__enter__.return_value.login.call_count == 0
    assert mocked_smtp.return_value.__enter__.return_value.sendmail.call_count == 0


def test_server_error(mocked_smtp, dao_with_adjusted_last_alerted):
    dao = dao_with_adjusted_last_alerted
    num_alerts = len(dao.get_all_alerts())
    mocked_smtp.return_value.__enter__.return_value.starttls.side_effect = smtplib.SMTPDataError(
        code=2, msg="Expected exception")
    alerts.send_alerts()
    assert num_alerts == len(dao.get_all_alerts())
