from flaskapp import create_app
from config import DevConfig


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
