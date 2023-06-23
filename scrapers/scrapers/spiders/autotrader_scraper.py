
# import requests
# from urllib.robotparser import RobotFileParser
# from bs4 import BeautifulSoup
# from db.body_styles import body_styles
from scrapy import Spider
import logging
from ..update_proxy_list import update_proxy_list
from scrapy import signals


logger = logging.getLogger("proxy_logger")
logger.setLevel(logging.INFO)
f_handler = logging.FileHandler("parse_info.log")
f_handler.setLevel(logging.INFO)
f_formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
f_handler.setFormatter(f_formatter)
logger.addHandler(f_handler)


class AutotraderScraper(Spider):
    name = "autotrader"

    start_urls = [
        "https://www.autotrader.com/cars-for-sale/all-cars?zip=50123"
    ]

    pages_visited = 0

    def parse(self, response):
        logger.info("in parse method")
        # logger.info(response.css("div").getall()[0])
        for listing in response.css("div.item-card-body"):
            logger.info(f"found listing: {listing}")

    def listing_parse(self, response):
        pass

    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        spider = super(AutotraderScraper, cls).from_crawler(
            crawler, *args, **kwargs)
        crawler.signals.connect(spider.spider_opened,
                                signal=signals.spider_opened)
        return spider

    def spider_opened(self):
        update_proxy_list()
