"""
1) Взять любую категорию товаров на сайте Леруа Мерлен. Собрать следующие данные:
- название;
- все фото;
- ссылка;
- цена.

Реализуйте очистку и преобразование данных с помощью ItemLoader. Цены должны быть в виде числового значения.
"""

import scrapy
from scrapy.http import HtmlResponse
from leroymerlin.items import LeroymerlinItem
from scrapy.loader import ItemLoader

class LeroymerlinruSpider(scrapy.Spider):
    name = 'leroymerlinru'
    allowed_domains = ['leroymerlin.ru']

    def __init__(self, name=None, **kwargs):
        super().__init__(name=name, **kwargs)
        self.start_urls = [f'https://spb.leroymerlin.ru/search/?q={kwargs.get("search")}']

    def parse(self, response: HtmlResponse):

        next_page = response.xpath("//a[@data-qa-pagination-item='right']/@href").get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)

        links = response.xpath("//a[@data-qa='product-name']")
        for link in links:
            yield response.follow(link, callback=self.parse_ads)

    def parse_ads(self, response: HtmlResponse):
        loader = ItemLoader(item=LeroymerlinItem(), response=response)
        loader.add_xpath('name', "//h1[@class='header-2']/text()")
        loader.add_xpath('photos', "//img[@alt='product image']/@src")
        loader.add_value('url', response.url)
        loader.add_xpath('price', "//span[@slot='price']/text()")
        yield loader.load_item()
