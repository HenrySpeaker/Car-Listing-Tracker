from spiders.spysone_scraper import SpysOneScraper
from spiders.autotrader_scraper import AutotraderScraper
from twisted.internet import defer, reactor
from scrapy.crawler import CrawlerProcess, CrawlerRunner

spysone_settings = {"DOWNLOADER_MIDDLEWARES": {'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,
                                               'scrapy_user_agents.middlewares.RandomUserAgentMiddleware': 400, }}
autotrader_settings = {"DOWNLOADER_MIDDLEWARES": {
    'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,
    'scrapy_user_agents.middlewares.RandomUserAgentMiddleware': 400,
    'rotating_proxies.middlewares.RotatingProxyMiddleware': 610,
    'rotating_proxies.middlewares.BanDetectionMiddleware': 620,
}}

spys_process = CrawlerProcess(spysone_settings)
autotrader_process = CrawlerProcess(autotrader_settings)


@defer.inlineCallbacks
def crawl():
    yield spys_process.crawl(SpysOneScraper)
    yield autotrader_process.crawl(AutotraderScraper)
    reactor.stop()


crawl()
reactor.run()
