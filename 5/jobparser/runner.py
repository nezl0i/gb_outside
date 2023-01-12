from twisted.internet import reactor
from scrapy.crawler import CrawlerRunner
from scrapy.utils.project import get_project_settings
from scrapy.utils.log import configure_logging

from spiders.hh_ru import HhRuSpider
from spiders.superjob_ru import SuperjobRuSpider
from spiders.rabota_ru import RabotaRuSpider

if __name__ == '__main__':
    configure_logging()
    settings = get_project_settings()
    runner = CrawlerRunner(settings)
    runner.crawl(HhRuSpider)
    runner.crawl(SuperjobRuSpider)
    runner.crawl(RabotaRuSpider)
    d = runner.join()
    d.addBoth(lambda _: reactor.stop())
    reactor.run()
