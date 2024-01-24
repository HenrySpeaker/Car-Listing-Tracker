from flask import Blueprint
from datacollection.find_cars import logger, find_cars_by_criteria_id


search_bp = Blueprint('site', __name__)


@search_bp.route("/search/<int:criteria_id>", methods=["POST"])
def search(criteria_id=None):
    logger.info(f"Searching for cars based on criteria id {criteria_id}")

    find_cars_by_criteria_id(criteria_id)

    return "Success", 200
