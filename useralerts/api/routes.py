from flask import Blueprint
from useralerts.alerts import logger, send_all_watched_cars, send_new_alerts


alerts_bp = Blueprint('site', __name__)


@alerts_bp.route("/alert-all/<int:criteria_id>", methods=["POST"])
def alert_all(criteria_id=None):
    logger.info(f"Sending alert for found cars based on criteria id {criteria_id}")

    send_all_watched_cars(criteria_id)

    return "Success", 200


@alerts_bp.route("/alert-new", methods=["POST"])
def alert_new():
    logger.info("Sending out all pending new listing and price drop alerts")

    send_new_alerts()

    return "Success", 200
