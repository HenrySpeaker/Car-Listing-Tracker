import logging
from flask import Blueprint, render_template, current_app, redirect, request
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_required, login_user, current_user, logout_user
from flaskapp.forms import RegisterForm, LoginForm, MakeModelCriteriaForm, BodyStyleCriteriaForm, ChangeAccountInfoForm
from db.dbi.db_interface import DBInterface
from flaskapp.user import User


criteria_map = {'min_year': 'Minimum year', 'max_year': 'Maximum year', 'min_price': 'Minimum price', 'max_price': 'Maximum price', 'max_mileage': 'Maximum mileage',
                'search_distance': 'Search radius', 'no_accidents': 'No accidents', 'single_owner': 'Single owner', 'make_name': 'Make', 'model_name': 'Model', 'body_style_name': 'Body style'}

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("routes_logger")
handler = logging.FileHandler("flaskapp/routes.log")
handler.setLevel(logging.DEBUG)
format = logging.Formatter('%(name)s - %(levelname)s - %(message)s')
handler.setFormatter(format)
logger.addHandler(handler)

bp = Blueprint('site', __name__)


@bp.route("/")
def home():
    return render_template("home.html")


@bp.route("/login", methods=["GET", "POST"])
def login():
    db_uri = current_app.config["POSTGRES_DATABASE_URI"]
    db_interface = DBInterface(db_uri)
    form = LoginForm()
    if form.validate_on_submit():
        user_info = {"username": form.username.data,
                     "email": form.email.data, "password": form.password.data}
        logger.info("login attempt")
        logger.info(user_info)

        if user_info["username"]:
            poss_user = db_interface.get_user_by_username(
                user_info["username"])
            if poss_user and check_password_hash(poss_user["password_hash"], user_info["password"]):
                new_user = User(user_id=poss_user["id"],
                                username=poss_user["username"])
                login_user(new_user)
                logger.info("new user logged in by username")
                logger.info(poss_user)
                return redirect("account")
            else:
                return redirect("login")

        elif user_info["email"]:
            poss_user = db_interface.get_user_by_email(
                user_info["email"])
            if poss_user and check_password_hash(poss_user["password_hash"], user_info["password"]):
                new_user = User(user_id=poss_user["id"],
                                username=poss_user["username"])
                login_user(new_user)
                logger.info("new user logged in by email")
                logger.info(poss_user)
                return redirect("account")
            else:
                return redirect("login")

        else:  # pragma: no cover
            return render_template("login.html", form=form)

    return render_template("login.html", form=form)


@bp.route("/register", methods=["GET", "POST"])
def register():
    logger.info("register path accessed")
    form = RegisterForm()
    db_uri = current_app.config["POSTGRES_DATABASE_URI"]
    db_interface = DBInterface(db_uri)
    if form.validate_on_submit():

        new_username = form.username.data
        new_email = form.email.data

        if db_interface.get_user_by_username(new_username) or db_interface.get_user_by_email(new_email):
            return redirect("/register")

        password_hash = generate_password_hash(form.password.data)
        user_info = {"username": form.username.data, "email": form.email.data,
                     "password_hash": password_hash, "notification_frequency": form.notification_frequency.data}
        db_interface.add_user(user_info=user_info)
        logger.info("Form validated")
        logger.info(user_info)

        return redirect("login")

    return render_template("register.html", form=form)


@bp.route("/account")
@login_required
def account():
    logger.info(f"User account accessed. User id: {current_user.user_id}")
    return render_template("account.html")


@bp.route("/criteria/<crit_id>", methods=["POST"])
@login_required
def criteria_remove(crit_id=None):

    db_uri = current_app.config["POSTGRES_DATABASE_URI"]
    db_interface = DBInterface(db_uri)
    logger.info(f"removing criteria {crit_id}")
    db_interface.delete_criteria_by_id(id=int(crit_id))

    return redirect("/criteria")


@bp.route("/criteria", methods=["GET"])
@login_required
def criteria():
    db_uri = current_app.config["POSTGRES_DATABASE_URI"]
    db_interface = DBInterface(db_uri)
    user_criteria = db_interface.get_criteria_by_user_id(
        user_id=current_user.user_id)

    criteria = [{
        "id": row["id"],
        "min_year": row["min_year"],
        "max_year": row["max_year"],
        "min_price": row["min_price"] if row["min_price"] else 0,
        "max_price": row["max_price"],
        "max_mileage": row["max_mileage"],
        "search_distance": row["search_distance"],
        "no_accidents": row["no_accidents"],
        "single_owner": row["single_owner"],
        "make_name": db_interface.get_make_by_id(db_interface.get_model_by_id(row["model_id"])["make_id"])["make_name"] if row["model_id"] else "No make",
        "model_name": model_info["model_name"] if row["model_id"] and (model_info := db_interface.get_model_by_id(row["model_id"])) else "No model",
        "body_style_name": body_style if row["body_style_id"] and (body_style := db_interface.get_body_style_by_id(row["body_style_id"])["body_style_name"]) else db_interface.get_body_style_by_id(db_interface.get_model_by_id(row["model_id"])["body_style_id"])["body_style_name"]

    } for row in user_criteria]

    key_list = list(criteria[0].keys()) if criteria else []

    if "id" in key_list:
        key_list.remove("id")

    logger.info(f"Criteria for user id: {current_user.user_id} accessed")

    return render_template("criteria.html", criteria=criteria, key_map=criteria_map, key_list=key_list, criteria_id_list=[row["id"] for row in user_criteria])


@bp.route("/add-criteria", methods=["GET", "POST"])
@login_required
def add_criteria():

    db_uri = current_app.config["POSTGRES_DATABASE_URI"]
    db_interface = DBInterface(db_uri)
    makes = db_interface.get_all_makes()
    makes.sort(key=lambda make: make["make_name"])

    logger.info(
        f"Add criteria page accessed by user id {current_user.user_id}")

    return render_template("add_criteria.html", makes=makes)


@bp.route("/add-criteria/body-style", methods=["GET", "POST"])
@login_required
def add_criteria_body_style():
    form = BodyStyleCriteriaForm()
    if form.validate_on_submit():
        db_uri = current_app.config["POSTGRES_DATABASE_URI"]
        db_interface = DBInterface(db_uri)
        criteria = {
            "min_year": form.min_year.data,
            "max_year": form.max_year.data,
            "min_price": form.min_price.data,
            "max_price": form.max_price.data,
            "max_mileage": form.max_mileage.data,
            "search_distance": form.search_distance.data,
            "no_accidents": form.no_accidents.data,
            "single_owner": form.single_owner.data,
            "user_id": current_user.user_id,
            "zip_code_id": db_interface.get_zip_code_info(form.zip_code.data)["id"],
            "model_id": None,
            "body_style_id": db_interface.get_body_style_info(form.body_style.data)["id"]
        }
        logger.info("new body style criteria submitted")
        logger.info(criteria)
        db_interface.add_criteria(**criteria)
        return redirect("/criteria")
    return render_template("add_body_style_criteria.html", form=form)


@bp.route("/add-criteria/<make>", methods=["GET", "POST"])
@login_required
def add_criteria_make_model(make):
    form = MakeModelCriteriaForm()

    db_uri = current_app.config["POSTGRES_DATABASE_URI"]
    db_interface = DBInterface(db_uri)

    models_list = db_interface.get_model_by_make_name(make)
    models_list.sort(key=lambda model: model["model_name"])

    form.model_name.choices = [model["model_name"] for model in models_list]

    if form.validate_on_submit():
        db_uri = current_app.config["POSTGRES_DATABASE_URI"]
        db_interface = DBInterface(db_uri)
        criteria = {
            "min_year": form.min_year.data,
            "max_year": form.max_year.data,
            "min_price": form.min_price.data,
            "max_price": form.max_price.data,
            "max_mileage": form.max_mileage.data,
            "search_distance": form.search_distance.data,
            "no_accidents": form.no_accidents.data,
            "single_owner": form.single_owner.data,
            "user_id": current_user.user_id,
            "zip_code_id": db_interface.get_zip_code_info(form.zip_code.data)["id"],
            "model_id": db_interface.get_model_by_name(form.model_name.data)["id"],
            "body_style_id": None
        }
        logger.info("new make/model criteria submitted")
        logger.info(criteria)
        db_interface.add_criteria(**criteria)
        return redirect("/criteria")

    return render_template("add_make_model_criteria.html", form=form, make=make)


@bp.route("/logout")
@login_required
def logout():
    logout_user()

    return redirect("/login")


@bp.route("/change-info", methods=["GET", "POST"])
@login_required
def change_info():
    db_uri = current_app.config["POSTGRES_DATABASE_URI"]
    db_interface = DBInterface(db_uri)

    user_info = db_interface.get_user_by_id((user_id := int(current_user.user_id)))

    class DefaultValues(object):
        username = user_info["username"]
        email = user_info["email"]
        notification_frequency = user_info["notification_frequency"]

    default_values = DefaultValues()

    info_form = ChangeAccountInfoForm(obj=default_values)

    if info_form.validate_on_submit():
        logger.info(f"updating user {user_id} information")

        new_username = info_form.username.data
        new_email = info_form.email.data

        if (possible_user := db_interface.get_user_by_username(new_username)) and possible_user["id"] != user_id:
            return redirect("/change-info")

        if (possible_user := db_interface.get_user_by_email(new_email)) and possible_user["id"] != user_id:
            return redirect("/change-info")

        user_info = {"id": user_id, "username": new_username, "email": new_email,
                     "notification_frequency": info_form.notification_frequency.data}

        db_interface.update_user_info(user_info)

        return redirect("/account")

    return render_template("change-info.html", form=info_form)
