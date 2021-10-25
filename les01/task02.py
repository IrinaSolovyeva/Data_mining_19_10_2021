"""
Изучить список открытых API. Найти среди них любое, требующее авторизацию (любого типа).
Выполнить запросы к нему, пройдя авторизацию. Ответ сервера записать в файл.
"""

import requests
import json

url = "https://api.github.com/user/emails"
username = input("Enter username:")
token = input("Enter token:")

request = requests.get(url, auth=(username, token))
info = request.json()

with open('task02.json', 'w', encoding='UTF-8') as f:
    json.dump(info, f, indent=4)

