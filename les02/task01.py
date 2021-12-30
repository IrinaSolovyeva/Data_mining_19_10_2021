"""
Необходимо собрать информацию о вакансиях на вводимую должность (используем input или через аргументы
получаем должность) с сайтов HH(обязательно) и/или Superjob(по желанию).
Приложение должно анализировать несколько страниц сайта (также вводим через input или аргументы).
Получившийся список должен содержать в себе минимум:

- Наименование вакансии.
- Предлагаемую зарплату (разносим в три поля: минимальная и максимальная и валюта. цифры преобразуем к цифрам).
- Ссылку на саму вакансию.
- Сайт, откуда собрана вакансия.

По желанию можно добавить ещё параметры вакансии (например, работодателя и расположение).
Структура должна быть одинаковая для вакансий с обоих сайтов. Общий результат можно вывести с помощью dataFrame
через pandas. Сохраните в json либо csv.
"""

from bs4 import BeautifulSoup
import requests
import pandas as pd
from pprint import pprint

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

        vacancy_data['name'] = name
        vacancy_data['link'] = link
        vacancy_data['salary_min'] = salary_min
        vacancy_data['salary_max'] = salary_max
        vacancy_data['salary_currency'] = salary_currency
        vacancies_list.append(vacancy_data)

    params['page'] += 1

#pprint(vacancies_list)

df = pd.DataFrame(vacancies_list)
df.to_csv("hh.csv", sep=";", index=False)
