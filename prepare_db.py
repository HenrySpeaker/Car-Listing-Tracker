from zipdata.add_geo_data_to_db import add_data
from datacollection.add_cars_to_db import add_models_to_db


def prepare_db():  # pragma: no cover
    add_data()
    add_models_to_db()


if __name__ == "__main__":  # pragma: no cover
    prepare_db()
