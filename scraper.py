from swa import *
from swa.spiders import *
from swa.settings import *

from twisted.internet import reactor
from scrapy.crawler import Crawler
from scrapy.settings import Settings
from scrapy.shell import Shell
from scrapy import log


swa = SWAFareSpider("AUS", "August 14th 2013", "PIT")
crawler = Crawler(Settings())
crawler.configure()
crawler.crawl(swa)
crawler.start()
log.start(loglevel=log.DEBUG)
reactor.run()
