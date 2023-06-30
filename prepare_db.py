from ZipData.add_geo_data_to_db import add_data
from dataCollection.add_cars import add_models_to_db


def prepare_db():
    add_data()
    add_models_to_db()


if __name__ == "__main__":
    prepare_db()
