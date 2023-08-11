import pytest
import alerts.alerts as alerts


@pytest.fixture
def mocked_smtp(mocker):
    mock_SMTP = mocker.MagicMock(name="alerts.smtplib.SMTP")
    mocker.patch("alerts.smtplib.SMTP", new=mock_SMTP)
