"""
Посмотреть документацию к API GitHub, разобраться как вывести список репозиториев для конкретного пользователя,
сохранить JSON-вывод в файле *.json.
"""

import requests
import json

username = input("Enter the github username:")
request = requests.get(f"https://api.github.com/users/{username}/repos")
repo_info = request.json()

for itm in repo_info:
    print("Repo name:", itm["name"])

with open('task01.json', 'w', encoding='UTF-8') as f:
    json.dump(repo_info, f, indent=4)
