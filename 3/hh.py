import re
import json
import requests
from time import sleep
from bs4 import BeautifulSoup as bs


headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
}

params = {'page': 0, 'hhtmFrom': 'vacancy_search_catalog'}
search = 'prodavets-konsultant'
site_name = 'https://hh.ru/vacancies/'
url = f'{site_name}{search}'
json_file = 'hh_result.json'
json_vacancies = list()

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

        json_vacancies.append({
            'Вакансия': name_link.text.replace('\n', '').strip(),
            'URL': 'h' + name_link['href'][1:],
            'Зарплата от': minimal_salary,
            'Зарплата до': maximal_salary,
            'Сайт': site_name})

    params['page'] += 1
    response = session.get(url, headers=headers, params=params)
    dom = bs(response.text, 'html.parser')
    side = dom.find_all('div', {'class': ['vacancy-serp-item-body__main-info']})

    sleep(5)

with open(json_file, 'w', encoding='UTF-8') as f:
    json.dump(json_vacancies, f, ensure_ascii=False)
    print(f'{json_file} создан!')
