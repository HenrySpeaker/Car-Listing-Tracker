import smtplib
from smtplib import SMTPRecipientsRefused, SMTPNotSupportedError, SMTPHeloError, SMTPDataError
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from config import ProdConfig
from db.dbi.db_interface import DBInterface
from collections import defaultdict
import logging
from jinja2 import Environment, FileSystemLoader
from collections import OrderedDict
from datetime import datetime

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
handler = logging.FileHandler("useralerts/alerts.log")
handler.setLevel(logging.DEBUG)
format = logging.Formatter('%(name)s - %(levelname)s - %(message)s')
handler.setFormatter(format)
logger.addHandler(handler)

EMAIL = ProdConfig.ALERTS_EMAIL
PASSWORD = ProdConfig.ALERTS_EMAIL_PASSWORD
DB_URI = ProdConfig.POSTGRES_DATABASE_URI
RETRY_LIMIT = ProdConfig.SMTP_RETRY_LIMIT

dbi = DBInterface(DB_URI)

new_alerts_column_order = OrderedDict()
new_alerts_column_order["make_name"] = "Make"
new_alerts_column_order["model_name"] = "Model"
new_alerts_column_order["model_year"] = "Model year"
new_alerts_column_order["current_price"] = "Current price"
new_alerts_column_order["previous_price"] = "Previous price"
new_alerts_column_order["url"] = "Link"

all_watched_cars_columns = OrderedDict()
all_watched_cars_columns["model_year"] = "Model year"
all_watched_cars_columns["last_price"] = "Current price"
all_watched_cars_columns["listing_url"] = "Link"
all_watched_cars_columns["last_update"] = "Last Updated"

email_template_environment = Environment(loader=FileSystemLoader("useralerts/templates/"))


class UserAlerts:

    def __init__(self):
        self.new_listings = []
        self.price_drops = []

    def add_new_listing(self, listing):
        self.new_listings.append(listing)

    def add_price_drop(self, listing):
        self.price_drops.append(listing)


def get_listing_details(listings: list[dict]):
    """
    Accepts a list of dictionaries representing alerts of a particular user. 
    The dictionaries are modified to hold additional key-value pairs of pertinent information for the alerts that wasn't stored in the same table.
    """

    for listing in listings:
        car_id = listing["car_id"]
        car_info = dbi.get_watched_car_by_id(id=car_id)
        listing["url"] = car_info["listing_url"]
        listing["current_price"] = f"${car_info['last_price']}"
        listing["previous_price"] = f"${car_info['prev_price']}"
        listing["model_year"] = car_info["model_year"]
        model_info = dbi.get_model_by_id(model_id=dbi.get_criteria_by_id(
            id=car_info["criteria_id"])["model_id"])
        listing["model_name"] = model_info["model_name"] if model_info else None
        listing["make_name"] = dbi.get_make_by_id(
            make_id=model_info["make_id"])["make_name"] if model_info else None

    return listings


def send_new_alerts():
    """
    Fetches all current alerts, attempts to send them to their respective users, and clears any alerts that were successfully sent.
    """
    alerts = dbi.get_all_alerts()

    user_alerts = defaultdict(UserAlerts)
    user_alerts_due = defaultdict(bool)

    car_id_to_user_id = {}

    for alert in alerts:
        if alert["car_id"] not in car_id_to_user_id:
            watched_car = dbi.get_watched_car_by_id(alert["car_id"])

            criteria = dbi.get_criteria_by_id(id=watched_car["criteria_id"])

            user_id = criteria["user_id"]

            car_id_to_user_id[alert["car_id"]] = user_id

            curr_dt = datetime.now()

            user_info = dbi.get_user_by_id(id=user_id)

            last_alerted = user_info["last_alerted"]

            tz = last_alerted.tzinfo

            curr_dt = curr_dt.astimezone(tz)

            time_difference = curr_dt - last_alerted

            notification_freq = user_info["notification_frequency"]

            user_alerts_due[user_id] = time_difference.total_seconds() > notification_freq * 86400 - \
                43200 or ProdConfig.IMMEDIATE_ALERT_OVERRIDE

        if not user_alerts_due[car_id_to_user_id[alert["car_id"]]]:
            continue

        if alert["change"] == "price_drop":
            user_alerts[car_id_to_user_id[alert["car_id"]]
                        ].add_price_drop(alert)
        else:
            user_alerts[car_id_to_user_id[alert["car_id"]]
                        ].add_new_listing(alert)

    html_template = email_template_environment.get_template("new_alerts_html_template.txt")
    text_template = email_template_environment.get_template("new_alerts_text_template.txt")

    with smtplib.SMTP("smtp.gmail.com", port=587) as connection:
        for user_id in user_alerts:
            new_listings = user_alerts[user_id].new_listings
            price_drops = user_alerts[user_id].price_drops

            new_listings = get_listing_details(new_listings)
            price_drops = get_listing_details(price_drops)

            html_body = html_template.render(
                new_listings=new_listings, price_drops=price_drops, columns=new_alerts_column_order)
            text_body = text_template.render(
                new_listings=new_listings, price_drops=price_drops, columns=new_alerts_column_order)

            user_email = dbi.get_user_by_id(id=user_id)["email"]

            if send_emails(connection, user_email, text_body, html_body, "New Listings and Price Drops", user_id):
                for car in new_listings:
                    dbi.delete_alerts_by_info(car_id=car["car_id"])

                for car in price_drops:
                    dbi.delete_alerts_by_info(car_id=car["car_id"])

                dbi.update_last_alerted_by_id(user_id, datetime.now())


def send_all_watched_cars(criteria_id: int):
    logger.info(f"Sending all watched cars from criteria {criteria_id}")

    listings = dbi.get_watched_car_by_criteria_id(criteria_id)

    for listing in listings:
        listing["last_update"] = listing["last_update"].strftime("%Y-%m-%d")
        listing["last_price"] = f"${listing['last_price']}"
    criteria_info = dbi.get_criteria_by_id(criteria_id)
    criteria_info["zip_code"] = dbi.get_zip_code_by_id(criteria_info["zip_code_id"])["zip_code"]
    if criteria_info["model_id"]:
        model_data = dbi.get_model_by_id(criteria_info["model_id"])

        criteria_info["model_name"] = model_data["model_name"]
        criteria_info["make_name"] = dbi.get_make_by_id(model_data["make_id"])["make_name"]
    else:
        criteria_info["body_style_name"] = dbi.get_body_style_by_id(criteria_info["body_style_id"])[
            "body_style_name"]

    user_info = dbi.get_user_by_id(criteria_info["user_id"])

    html_body = email_template_environment.get_template("all_alerts_html_template.txt").render(
        listings=listings, columns=all_watched_cars_columns, criteria_info=criteria_info)
    text_body = email_template_environment.get_template("all_alerts_text_template.txt").render(
        listings=listings, columns=all_watched_cars_columns, criteria_info=criteria_info)

    with smtplib.SMTP("smtp.gmail.com", port=587) as connection:
        send_emails(connection, user_info["email"], text_body, html_body, "Full Search Results", user_info["id"])


def send_emails(connection: smtplib.SMTP, user_email: str, text_body: str, html_body: str, subject: str, user_id: int) -> bool:
    email = MIMEMultipart("alternative")
    email["Subject"] = subject
    email["From"] = EMAIL
    email["To"] = user_email

    email.attach(MIMEText(text_body, "plain"))
    email.attach(MIMEText(html_body, "html"))

    logger.info(
        f"Alerting user {user_id} of {subject}")

    num_tries = 0

    while num_tries < RETRY_LIMIT:

        try:
            connection.starttls()
            connection.login(user=EMAIL, password=PASSWORD)

            connection.sendmail(
                from_addr=EMAIL,
                to_addrs=user_email,
                msg=email.as_string(),
            )

            break

        except (SMTPRecipientsRefused, SMTPNotSupportedError, SMTPHeloError, SMTPDataError) as error:
            logger.error(
                f"email alerts to user {user_id} failed with error {error}")

        num_tries += 1

    return num_tries < RETRY_LIMIT
