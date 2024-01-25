import requests
import logging
import time
import datetime as dt
from scheduler import Scheduler
from config import ProdConfig

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("scheduler_logger")
handler = logging.FileHandler("routes.log")
handler.setLevel(logging.DEBUG)
format = logging.Formatter('%(name)s - %(levelname)s - %(message)s')
handler.setFormatter(format)
logger.addHandler(handler)


def run_events():
    logger.info(f"Running events at {dt.datetime.now()}")

    response = requests.post(f"http://{ProdConfig.SEARCH_SERVICE_NAME}:{ProdConfig.SEARCH_PORT}/search-all")

    try:
        response.raise_for_status()
    except Exception as e:
        logger.info(f"Scheduled start search failed with exception {e}")

    alert_response = requests.post(
        f"http://{ProdConfig.ALERTS_SERVICE_NAME}:{ProdConfig.ALERTS_PORT}/alert-new/0")

    try:
        alert_response.raise_for_status()
    except Exception as e:
        logger.info(f"Scheduled send new/price drop alerts failed with exception {e}")


schedule = Scheduler()

schedule.cyclic(dt.timedelta(seconds=float(ProdConfig.SCHEDULE_CYCLE)), run_events)

while True:
    schedule.exec_jobs()
    time.sleep(1)
