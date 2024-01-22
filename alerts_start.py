import datetime
from useralerts.alerts import send_alerts, logger

if __name__ == "__main__":
    logger.info(f"Starting user alerts script at {datetime.datetime.utcnow()}")
    send_alerts()
