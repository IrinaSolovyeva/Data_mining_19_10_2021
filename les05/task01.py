"""
Вариант II
2) Написать программу, которая собирает товары «В тренде» с сайта техники mvideo и складывает данные в БД.
Сайт можно выбрать и свой. Главный критерий выбора: динамически загружаемые товары
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from pymongo import MongoClient

client = MongoClient('127.0.0.1', 27017)
db = client['mvideo']

mvideo_trends = db.mvideo

chrome_options = Options()
chrome_options.add_argument('start-maximized')

driver = webdriver.Chrome(options=chrome_options)

driver.get('https://www.mvideo.ru/')

driver.implicitly_wait(10)
driver.execute_script("window.scrollTo(0, 1080)")

button = driver.find_element(By.XPATH, "//span[contains(text(),'В тренде')]")
button.click()

trends = driver.find_elements(By.TAG_NAME, 'mvid-product-cards-group')[1]
names = trends.find_elements(By.XPATH, ".//div[contains(@class, 'product-mini-card__name')]")
prices = trends.find_elements(By.XPATH, ".//div[contains(@class, 'product-mini-card__price')]")

data = []
for name, price in zip(names, prices):
    data.append({
        'name': name.find_element(By.XPATH, "./div/a/div").text,
        'price': price.find_element(By.XPATH, ".//span[@class='price__main-value']").text
        })

mvideo_trends.insert_many(data)

driver.quit()
