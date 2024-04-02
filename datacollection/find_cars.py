from datetime import datetime
from config import ProdConfig
from db.dbi.db_interface import DBInterface
from db.body_styles import body_styles
from datacollection.iseecars import get_iseecars_listings
from datacollection.dc_logger import logger

dbi_url = ProdConfig.POSTGRES_DATABASE_URI

dbi = DBInterface(dbi_url)


def find_cars_by_criteria_id(criteria_id: int):
    criteria = dbi.get_criteria_by_id(criteria_id)
    # add make and model once to avoid each website query using the same DB queries
    if criteria["model_id"]:
        criteria["model"] = dbi.get_model_by_id(criteria["model_id"])["model_name"]
        criteria["make"] = dbi.get_make_by_id(
            make_id=dbi.get_model_by_id(model_id=criteria["model_id"])["make_id"])["make_name"]
    else:
        criteria["model"] = ""
        criteria["make"] = ""

    if criteria["body_style_id"]:
        criteria["body_style"] = dbi.get_body_style_by_id(
            criteria["body_style_id"])["body_style_name"]

        criteria["isc_body_style"] = body_styles[criteria["body_style"]]["iseecars"]
    else:
        criteria["body_style"] = ""
        criteria["isc_body_style"] = ""

    criteria["zip_code"] = dbi.get_zip_code_by_id(
        criteria["zip_code_id"])["zip_code"]

    isc_listings = get_iseecars_listings(criteria)

    for car in isc_listings:
        res = dbi.get_watched_car_by_vin(car["vin"])

        # if car in db then update the listing if necessary and add listing to alerts table if necessary
        if res and res["last_price"] > car["price"]:

            # first check and see if any previous price drops are in the alerts table and clear them
            possible_prev_alerts = dbi.get_alert_by_info(car_id=res["id"])

            if possible_prev_alerts:
                dbi.delete_alerts_by_info(car_id=res["id"])

            dbi.add_alert(car_id=res["id"], change="price_drop")

            dbi.update_watched_car(
                vin=car["vin"], last_price=car["price"], last_update=datetime.now(), prev_price=res["last_price"])

        # if car not in db then add it and update alerts table
        elif not res and len(car["url"]) <= 500:
            max_mileage = criteria["max_mileage"]

            if car["mileage"] > max_mileage:
                continue

            logger.info(f"adding car with vin {car['vin']}")

            dbi.add_watched_car(
                vin=car["vin"], listing_url=car["url"], last_price=car["price"], criteria_id=criteria["id"], model_year=car["model_year"])
            res = dbi.get_watched_car_by_vin(vin=car["vin"])
            dbi.add_alert(car_id=res["id"], change="new_listing")


def find_cars():
    """
    Finds cars that match current criteria, adds them to the watched car table if necessary, and creates any necessary alerts.
    """

    for criteria in dbi.get_all_criteria():
        find_cars_by_criteria_id(criteria["id"])


if __name__ == "__main__":  # pragma: no cover
    find_cars()
