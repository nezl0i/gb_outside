import requests
import re
from bs4 import BeautifulSoup as bs
from time import sleep
from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError

headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36'
}

client = MongoClient('127.0.0.1', 27017)
db = client['vacancies']

db.drop_collection('data')
db.drop_collection('duplicate_db')

data = db.data
duplicate_db = db.duplicate


def collect_data(name, link, min_salary, max_salary, site):
    success_status, failure_status = 0, 0
    obj = {'_id': f'{link.split("?")[0].split("/vacancy/")[1]}',
           'Вакансия': name,
           'URL': f'h{link}',
           'Зарплата от': min_salary,
           'Зарплата до': max_salary,
           'Сайт': site}
    try:
        data.insert_one(obj)
        success_status = 1
    except DuplicateKeyError:
        duplicate = {
            'Вакансия': name,
            'URL': f'h{link}'
        }
        duplicate_db.insert_one(duplicate)
        print(f'Дубль! вакансия "{name}" уже есть в базе')
        failure_status = 1
    return obj, success_status, failure_status


params = {'page': 0, 'hhtmFrom': 'vacancy_search_catalog'}
search = 'prodavets-konsultant'
site_name = 'https://hh.ru/vacancies/'
url = f'{site_name}{search}'
json_file = 'hh_result.json'
json_vacancies = list()

print('Start parsing...')

session = requests.Session()
response = session.get(url, headers=headers, params=params)

dom = bs(response.text, 'html.parser')
side = dom.find_all('div', {'class': ['vacancy-serp-item-body__main-info']})

while len(side) > 0:
    print(f"Parsing.. Страница - {params['page'] + 1}")

    for item in side:
        minimal_salary = None
        maximal_salary = None

        name_link = item.find('a', {'data-qa': 'serp-item__title'})
        vacancy = item.find('span', {'data-qa': 'vacancy-serp__vacancy-compensation'})
        if vacancy:
            salary = re.findall('(\d+)', vacancy.text)
            if len(salary) == 2:
                if not vacancy.text.find('до'):
                    maximal_salary = int(salary[0] + salary[1])
                else:
                    minimal_salary = int(salary[0] + salary[1])
            elif len(salary) == 0:
                pass
            else:
                minimal_salary = int(salary[0] + salary[1])
                maximal_salary = int(salary[2] + salary[3])

            json_vacancies, success, failure = collect_data(name_link.text.replace('\n', '').strip(),
                                                            name_link['href'][1:], minimal_salary, maximal_salary,
                                                            site_name)

    params['page'] += 1
    response = session.get(url, headers=headers, params=params)
    dom = bs(response.text, 'html.parser')
    side = dom.find_all('div', {'class': ['vacancy-serp-item-body__main-info']})

    sleep(5)

for d in data.find():
    print(d)
