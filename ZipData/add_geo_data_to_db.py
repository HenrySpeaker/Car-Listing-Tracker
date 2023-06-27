from db.dbi.db_interface import DBInterface
from config import ProdConfig
from csv import DictReader

dbi = DBInterface(ProdConfig.POSTGRES_DATABASE_URI)
file_location = "ZipData/zips.csv"


def get_geo_data():  # pragma: no cover
    with open(file_location) as file:
        reader = DictReader(file)
        rows = [row for row in reader]
    return rows


def add_data():  # pragma: no cover
    states = {}
    cities = {}
    zips = {}

    rows = get_geo_data()
    for row in rows:
        if row["state"] not in states:
            if not dbi.get_state_by_name(row["state"]):
                dbi.add_state(row["state"])
            states[row["state"]] = dbi.get_state_by_name(
                state_name=row["state"])["id"]

        if row["city"] not in cities:
            if not dbi.get_city_id(row["city"]):
                dbi.add_city(city_name=row["city"],
                             state_id=states[row["state"]])
            cities[row["city"]] = dbi.get_city_id(row["city"])

        if not dbi.get_zip_code_info(row["zip"]):
            dbi.add_zip_code(
                zip_code=row["zip"], city_id=cities[row["city"]])

    return rows, states, cities


if __name__ == "__main__":  # pragma: no cover
    add_data()
