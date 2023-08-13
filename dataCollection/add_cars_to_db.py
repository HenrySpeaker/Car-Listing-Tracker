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

    dbi.delete_all_models()
    dbi.delete_all_makes()
    dbi.delete_all_body_styles()

    make_ids = {}
    body_style_ids = {}

    # add body styles
    for body_style in body_styles:
        dbi.add_body_style(body_style_name=body_style)
        body_style_ids[body_style] = dbi.get_body_style_info(
            body_style_name=body_style)["id"]

    with open("car-data/all-models.csv", "r") as file:
        reader = DictReader(file)
        models_list = []

        for row in reader:
            if row["make"] not in make_ids:
                dbi.add_make(make_name=row["make"])
                make_ids[row["make"]] = dbi.get_make_info(
                    make_name=row["make"])["id"]

            db_row = {}
            db_row["model_name"] = row["model"]
            db_row["make_id"] = make_ids[row["make"]]
            db_row["body_style_id"] = body_style_ids[row["body_style"]]

            models_list.append(db_row)

            # 100 chosen as the interval based on local testing but a different interval may be more appropriate on other machines
            if len(models_list) == 100:
                dbi.add_models(models_list)
                models_list = []

        # add any remaining models
        if models_list:  # pragma: no cover
            dbi.add_models(models_list)


if __name__ == "__main__":  # pragma: no cover
    add_models_to_db()
