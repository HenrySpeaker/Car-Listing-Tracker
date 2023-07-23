from config import ProdConfig
from db.dbi.db_interface import DBInterface
from dataCollection.iseecars import get_iseecars_listings
from db.body_styles import body_styles

dbi_url = ProdConfig.POSTGRES_DATABASE_URI\

dbi = DBInterface(dbi_url)


def find_cars():
    # iterate over criteria

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
                crit["body_style_id"])

            crit["isc_body_style"] = body_styles[crit["body_style"]]["iseecars"]
        else:
            crit["body_style"] = ""
            crit["isc_body_style"] = ""

        crit["zip_code"] = dbi.get_zip_code_by_id(
            crit["zip_code_id"])["zip_code"]

        # search for all matching cars
        isc_listings = get_iseecars_listings(crit)

        for car in isc_listings:
            # check if car is in db or not

            # if car in db then update the listing if necessary and add listing to alerts table if necessary

            # if car not in db then add it and update alerts table

            continue


if __name__ == "__main__":
    find_cars()
