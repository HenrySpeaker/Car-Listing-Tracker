from db.dbi.db_interface import DBInterface
from db.body_styles import body_styles
from csv import DictReader
from config import DevConfig, MODEL_ROW_COUNT

db_uri = DevConfig.POSTGRES_DATABASE_URI

dbi = DBInterface(db_uri)


def add_models_to_db():
    """Clears DB body style, make, and model contents and adds all contents from the raw car model data"""

    if dbi.get_model_count() == MODEL_ROW_COUNT:  # pragma: no cover
        return

    dbi.delete_all_body_styles()
    dbi.delete_all_makes()
    dbi.delete_all_models()

    make_ids = {}
    body_style_ids = {}
    # add body styles
    for body_style in body_styles:
        dbi.add_body_style(body_style_name=body_style)
        body_style_ids[body_style] = dbi.get_body_style_info(
            body_style_name=body_style)["id"]

    with open("car-data/all-models.csv", "r") as file:
        reader = DictReader(file)

        for row in reader:
            if row["make"] not in make_ids:
                dbi.add_make(make_name=row["make"])
                make_ids[row["make"]] = dbi.get_make_info(
                    make_name=row["make"])["id"]

            dbi.add_model(model_name=row["model"],
                          make_id=make_ids[row["make"]], body_style_id=body_style_ids[row["body_style"]])


if __name__ == "__main__":  # pragma: no cover
    add_models_to_db()
