from bs4 import BeautifulSoup as bs
import requests
from pprint import pprint

URL = 'https://hh.ru'
HEADERS = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36',
          'Accept':'*/*'}
area = 1
st = 'searchVacancy'
text = input('Введите текст вакансии:\n')

params = {'area': 'area', 'st': 'st', 'text': 'text', 'page': None}
#next_button = soup.find('a', {'class': 'HH-Pager-Controls-Next'}).getText()
def salary(string):
    if '-' in string:
        min = string.split('-')[0]
        _ = string.split()
        max = _[0].split('-')[1]
        currency = string.split()[1]
    if 'от' in string:
        min = string.split()[1]
        max = '-'
        currency = string.split()[2]
    if 'до' in string:
        max = string.split()[1]
        min = '-'
        currency = string.split()[2]
    if string == '':
        min = '-'
        max = '-'
        currency = '-'
    return {'min_salary': min , 'max_salary': max, 'currency': currency}

def get_html(url):
    request = requests.get(url + '/search/vacancy', headers=HEADERS, params=params)
    if request.status_code == 200:
        request =  (request.text)
    else:
        request = 'Что-то пошло не так'
    return request

def get_pages_count(soup):
    pagination = soup.find('a', {'class': 'HH-Pager-Control'}).getText()
    if pagination:
        return int(pagination)
    else:
        return 0

def get_content(soup):
    vacancy_list = soup.find_all('div', {'class': 'vacancy-serp-item'})
    vacancies = []
    for vacancy in vacancy_list:
        vacancies.append({
            'name': vacancy.find('a', {'class': 'bloko-link HH-LinkModifier'}).getText(),
            'link': vacancy.find('a', {'class': 'bloko-link HH-LinkModifier'})['href'],
            'salary': salary(vacancy.find('div', {'class': 'vacancy-serp-item__sidebar'}).getText().replace(u'\xa0', u''))
        })
    return vacancies


def parse(url):
    html = get_html(url)
    soup = bs(html, 'html.parser')
    pages_count = get_pages_count(soup)
    vacancies = []
    for page in range(0, pages_count + 1):
        print(f'Парсинг страницы {page + 1} из {pages_count + 1}...')
        soup = bs(requests.get(URL + '/search/vacancy', headers=HEADERS, params={'area': 'area', 'st': 'st', 'text': 'text', 'page': page}).text, 'html.parser')
        vacancies.extend(get_content(soup))

    return vacancies

pprint(parse(URL))