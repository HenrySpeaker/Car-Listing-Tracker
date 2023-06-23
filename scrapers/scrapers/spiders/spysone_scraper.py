from scrapy import Spider
import logging

logger = logging.getLogger("proxy_logger")
logger.setLevel(logging.INFO)
f_handler = logging.FileHandler("parse_info.log")
f_handler.setLevel(logging.INFO)
logger.addHandler(f_handler)


class SpysOneScraper(Spider):
    name = "spysone"

    start_urls = ["https://spys.one/en/anonymous-proxy-list/"]

    proxy_set = set()

    def parse(self, response):
        # fetch proxies, check for uptime >= 50%, and then add them to the set of proxies
        # if there are at least 10 proxies found then stop scraping
        rows = response.css("tr.spy1x").getall()[
            1:] + response.css("tr.spy1xx").getall()

        for row in rows:
            self.write_proxies(row)

    def write_proxies(self, row_contents):
        # proxy_path = self.settings.get('ROTATING_PROXY_LIST_PATH', None)
        # logger.info(f"setting for proxy path: {proxy_path}")

        logger.info(f"proxy row info {row_contents}")
