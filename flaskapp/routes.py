from flask import Blueprint, render_template, request, current_app, redirect
from .forms import RegisterForm, LoginForm, CriteriaForm
import logging
from werkzeug.security import generate_password_hash, check_password_hash
from db.dbi.db_interface import DBInterface
from flask_login import login_required, login_user, current_user
from .user import User

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
                return render_template("login.html", form=form)

        if user_info["email"]:
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
                return render_template("login.html", form=form)

    return render_template("login.html", form=form)


@bp.route("/register", methods=["GET", "POST"])
def register():
    logger.info("register path accessed")
    form = RegisterForm()
    db_uri = current_app.config["POSTGRES_DATABASE_URI"]
    db_interface = DBInterface(db_uri)
    if form.validate_on_submit():
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
    return render_template("account.html")


@bp.route("/criteria")
@login_required
def criteria():
    db_uri = current_app.config["POSTGRES_DATABASE_URI"]
    db_interface = DBInterface(db_uri)
    user_criteria = db_interface.get_all_criteria()
    key_list = user_criteria[0].keys() if user_criteria else []
    return render_template("criteria.html", criteria=user_criteria, key_list=key_list)


@bp.route("/add-criteria", methods=["GET", "POST"])
@login_required
def add_criteria():
    form = CriteriaForm()
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
        logger.info("new criteria submitted")
        logger.info(criteria)
        db_interface.add_criteria(**criteria)
        return redirect("criteria")
    return render_template("add_criteria.html", form=form)
