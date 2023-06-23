from flask import Blueprint, render_template, request, current_app, redirect
from .forms import RegisterForm
import logging
from werkzeug.security import generate_password_hash, check_password_hash
from db.dbi.db_interface import DBInterface
from flask_login import login_required

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("routes_logger")
handler = logging.FileHandler("flaskapp/routes.log")
handler.setLevel(logging.DEBUG)
format = logging.Formatter('%(name)s - %(levelname)s - %(message)s')
handler.setFormatter(format)
logger.addHandler(handler)

bp = Blueprint('site', __name__)

db_interface = DBInterface()


@bp.route("/")
def home():
    return render_template("home.html")


@bp.route("/login")
def login():
    return render_template("login.html")


@bp.route("/register", methods=["GET", "POST"])
def register():
    logger.info("register path accessed")
    form = RegisterForm()
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
    return render_template("criteria.html")


@bp.route("/add-criteria", methods=["GET", "POST"])
@login_required
def add_criteria():
    return render_template("add_criteria.html")
