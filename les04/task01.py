"""
1. Написать приложение, которое собирает основные новости с сайта на выбор news.mail.ru, lenta.ru, yandex-новости.
Для парсинга использовать XPath. Структура данных должна содержать:
    - название источника;
    - наименование новости;
    - ссылку на новость;
    - дата публикации.
2. Сложить собранные новости в БД

Минимум один сайт, максимум - все три
"""

from lxml import html
import requests
from pymongo import MongoClient
from pymongo.errors import *
from pprint import pprint

client = MongoClient('127.0.0.1', 27017)
db = client['news_lenta']

db_news = db.news_lenta

header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36'}

response = requests.get('https://lenta.ru/', headers=header)

dom = html.fromstring(response.text)

news_list = []

items = dom.xpath("//div[contains(@class, 'topnews__column')]//a[contains(@class, '_topnews')]")
for item in items:
    news = {}
    name = item.xpath(".//span[contains(@class, 'card-mini__title')]/text() | .//h3[contains(@class, 'card-big__title')]/text()")
    link = item.xpath("./@href")
    date = item.xpath(".//time[contains(@class,'card-big__date') or contains(@class,'card-mini__date')]/text()")

    news['sourse'] = 'https://lenta.ru'
    news['name'] = name[0]
    news['link'] = news['sourse'] + link[0]
    news['date'] = date[0]

    news_list.append(news)

    try:
        db_news.insert_one(news)
    except DuplicateKeyError:
        pass

pprint(news_list)
