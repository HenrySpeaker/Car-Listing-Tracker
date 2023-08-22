from config import ProdConfig
from db.dbi.db_interface import DBInterface
from datacollection.iseecars import get_iseecars_listings
from db.body_styles import body_styles
from datetime import datetime

dbi_url = ProdConfig.POSTGRES_DATABASE_URI

dbi = DBInterface(dbi_url)


def find_cars():

    for crit in dbi.get_all_criteria():

        # add make and model once to avoid each website query using the same DB queries
        if crit["model_id"]:
            crit["model"] = dbi.get_model_by_id(crit["model_id"])["model_name"]
            crit["make"] = dbi.get_make_by_id(
                make_id=dbi.get_model_by_id(model_id=crit["model_id"])["make_id"])["make_name"]
        else:
            crit["model"] = ""
            crit["make"] = ""

        if crit["body_style_id"]:
            crit["body_style"] = dbi.get_body_style_by_id(
                crit["body_style_id"])["body_style_name"]

            crit["isc_body_style"] = body_styles[crit["body_style"]]["iseecars"]
        else:
            crit["body_style"] = ""
            crit["isc_body_style"] = ""

        crit["zip_code"] = dbi.get_zip_code_by_id(
            crit["zip_code_id"])["zip_code"]

        isc_listings = get_iseecars_listings(crit)

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
                max_mileage = crit["max_mileage"]

                if car["mileage"] > max_mileage:
                    continue

                dbi.add_watched_car(
                    vin=car["vin"], listing_url=car["url"], last_price=car["price"], criteria_id=crit["id"], model_year=car["model_year"])
                res = dbi.get_watched_car_by_vin(vin=car["vin"])
                dbi.add_alert(car_id=res["id"], change="new_listing")


if __name__ == "__main__":  # pragma: no cover
    find_cars()
