import datetime
from dataCollection.find_cars import find_cars, logger

if __name__ == "__main__":
    logger.info(f"Starting car search script at {datetime.datetime.utcnow()}")
    find_cars()
