from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings

from leroymerlin.spiders.leroymerlinru import LeroymerlinruSpider
from leroymerlin import settings

if __name__ == '__main__':
    crawler_settings = Settings()
    crawler_settings.setmodule(settings)

    process = CrawlerProcess(settings=crawler_settings)
    process.crawl(LeroymerlinruSpider, search='дренажные насосы')

    process.start()
