from pymongo import MongoClient
from bs4 import BeautifulSoup as bs
import requests
from pprint import pprint
import json

URL = 'https://hh.ru'
HEADERS = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36',
          'Accept':'*/*'}
area = 1
st = 'searchVacancy'
text = input('Введите текст вакансии:\n')
clusters = True
enable_snippets = True
params = {'area': 'area',
          'st': 'st',
          'clusters': 'clusters',
          'enable_snippets': 'enable_snippets'}

def salary(string):
    if '-' in string:
        min = int(string.split('-')[0])
        _ = string.split()
        max = int(_[0].split('-')[1])
        currency = string.split()[1]
    if 'от' in string:
        min = int(string.split()[1])
        max = None
        currency = string.split()[2]
    if 'до' in string:
        max = int(string.split()[1])
        min = None
        currency = string.split()[2]
    if string == '':
        min = None
        max = None
        currency = None
    return {'min_salary': min , 'max_salary': max, 'currency': currency}

def get_html(url):
    request = requests.get(url + '/search/vacancy', headers=HEADERS, params=params)
    if request.status_code == 200:
        request =  (request.text)
    else:
        request = 'Что-то пошло не так'
    return request

def get_content(soup):
    vacancy_list = soup.find_all('div', {'class': 'vacancy-serp-item'})
    vacancies = []
    for vacancy in vacancy_list:
        vacancies.append({
            'name': vacancy.find('a', {'class': 'bloko-link HH-LinkModifier'}).getText(),
            'link': vacancy.find('a', {'class': 'bloko-link HH-LinkModifier'})['href'].split('?')[0],
            'salary': salary(vacancy.find('div', {'class': 'vacancy-serp-item__sidebar'}).getText().replace(u'\xa0', u''))
        })
    return vacancies

def parse(url):
    page = 0
    pages = []
    while True:
        html = get_html(url)
        soup = bs(html, 'html.parser')
        print(f'Парсинг страницы {page + 1} ...')
        soup = bs(requests.get(URL + '/search/vacancy', headers=HEADERS, params={'area': 1, 'st': 'searchVacancy', 'text': text, 'page': page}).text, 'html.parser')
        pages.extend(get_content(soup))
        page = page + 1
        if not soup.find('a', {'class': 'HH-Pager-Controls-Next'}):
            break
    return pages

data = (parse(URL))

def mongo_insert_hh(data):
    client = MongoClient('localhost', 27017)
    db = client['database']
    hh = db.hh
    hh.insert_many(data)

(mongo_insert_hh(data))

def salary_hh(data):
    client = MongoClient('localhost', 27017)
    db = client['database']
    hh = db.hh
    hh.insert_many(data)
    while True:
        salary = input('Введите зарплату:\n')
        if salary.isdigit():
            salary = int(salary)
            for item in hh.find({'salary.max_salary': {'$gte': salary}}, {'name': 1, 'salary.max_salary' :1, 'salary.min_salary' :1, 'link': 1, '_id': 0}):
                pprint(item)
            for item in hh.find({'salary.min_salary': {'$gte': salary}}, {'name': 1, 'salary.max_salary' :1, 'salary.min_salary' :1, 'link': 1, '_id': 0}):
                pprint(item)
            break
        else:
            print('Введено не число')

pprint(salary_hh(data))

