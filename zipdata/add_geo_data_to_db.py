from db.dbi.db_interface import DBInterface
from config import ProdConfig
from csv import DictReader
from config import ZIP_ROW_COUNT

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

    if dbi.get_zip_code_count() == ZIP_ROW_COUNT:
        return

    rows = get_geo_data()
    zips_list = []

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
            zips_list.append({"zip_code": row["zip"], "city_id": cities[row["city"]]})

        if len(zips_list) == 100:
            dbi.add_zip_codes(zips_list)
            zips_list = []

    if len(zips_list) > 0:
        dbi.add_zip_codes(zips_list)

    return rows, states, cities


if __name__ == "__main__":  # pragma: no cover
    add_data()
