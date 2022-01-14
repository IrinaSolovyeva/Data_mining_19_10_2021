"""
1. Развернуть у себя на компьютере/виртуальной машине/хостинге MongoDB и реализовать функцию,
которая будет добавлять только новые вакансии/продукты в вашу базу.
2. Написать функцию, которая производит поиск и выводит на экран вакансии с заработной платой больше введённой суммы
(необходимо анализировать оба поля зарплаты).
"""

from bs4 import BeautifulSoup
import requests
import pandas as pd
from pprint import pprint
from pymongo import MongoClient
from pymongo.errors import *
import re

client = MongoClient('127.0.0.1', 27017)
db = client['hh_vacancies']

db_vacancies = db.db_vacancies

url = 'https://spb.hh.ru'

params = {'text': 'Python',
          'page': 0}

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36'}

vacancies_list = []

while True:

    response = requests.get(url + '/search/vacancy', params=params, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')

    if not soup.find('a', {'data-qa': 'pager-next'}):
        break

    vacancies = soup.find_all('div', {'class': 'vacancy-serp-item'})

    for vacancy in vacancies:
        vacancy_data = {}
        salary_min = None
        salary_max = None
        salary_currency = None
        info = vacancy.find('a', {'data-qa': 'vacancy-serp__vacancy-title'})
        name = info.text
        link = info.get('href')
        vacancy_id = re.search(r'\d+', link).group(0)
        salary_info = vacancy.find('span', {'data-qa': 'vacancy-serp__vacancy-compensation'})

        if salary_info:
            salary = str(salary_info.text).split(' ')
            if salary[0] == 'от':
                salary_min = float(salary[1].replace(u'\u202f', ''))
                salary_max = None
                salary_currency = salary[-1]
            elif salary[0] == 'до':
                salary_min = None
                salary_max = float(salary[1].replace(u'\u202f', ''))
                salary_currency = salary[-1]
            else:
                salary_min = float(salary[0].replace(u'\u202f', ''))
                salary_max = float(salary[-2].replace(u'\u202f', ''))
                salary_currency = salary[-1]
        else:
            salary_min = None
            salary_max = None
            salary_currency = None

        vacancy_data['_id'] = vacancy_id
        vacancy_data['name'] = name
        vacancy_data['link'] = link
        vacancy_data['salary_min'] = salary_min
        vacancy_data['salary_max'] = salary_max
        vacancy_data['salary_currency'] = salary_currency
        vacancies_list.append(vacancy_data)

        try:
            db_vacancies.insert_one(vacancy_data)
        except DuplicateKeyError:
            pass

    params['page'] += 1

# df = pd.DataFrame(vacancies_list)
# df.to_csv("hh.csv", sep=";", index=False)

user_salary = float(input('Введите интересующую заработную плату: '))

def print_salary(my_salary):
    objects = db_vacancies.find({'$or': [{'salary_min': {'$gt': my_salary}}, {'salary_max': {'$gt': my_salary}}]})
    for obj in enumerate(objects):
        pprint(obj)

print_salary(user_salary)
