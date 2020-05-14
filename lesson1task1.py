from pprint import pprint
import requests
import json

URL = 'https://api.github.com/user/repos'

header = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.4 Safari/605.1.15',
'Accept': '*/*'}

username = input('Введите ваш логин:\n')
password = input('Введите ваш пароль:\n')

response = requests.get(URL, headers=header, auth=(username, password))

if response.ok:
    print(f'Вы вошли в личный кабинет портала Github пользователя {username}\nНазвания репозиториев:\n')
    data = json.loads(response.text)

for item in data:
    print(item['name'])