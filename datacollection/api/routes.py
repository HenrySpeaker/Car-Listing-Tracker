from flask import Blueprint
from datacollection.find_cars import logger, find_cars_by_criteria_id, find_cars


search_bp = Blueprint('site', __name__)


@search_bp.route("/search/<int:criteria_id>", methods=["POST"])
def search_by_criteria_id(criteria_id=None):
    logger.info(f"Searching for cars based on criteria id {criteria_id}")

    find_cars_by_criteria_id(criteria_id)

    return "Success", 200


@search_bp.route("/search-all", methods=["POST"])
def search_all():
    logger.info("Searching for cars from all criteria")

    find_cars()

    return "Success", 200
