import json
import requests


# URL from search
url = 'https://www.delivery-club.ru/eats/v1/full-text-search/v1/search'

# URL from company
url_vendors = 'https://www.delivery-club.ru/eats/v1/layout-constructor/v1/layout'

headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
    'content-type': 'application/json;charset=UTF-8',
    "x-device-id": "lblq22s5-iryf799j28-ozlwheqnj6f-83d03nqozdw"
}

session = requests.Session()
session.headers.update(headers)

params = {"text": "пицца", "location": {"longitude": 38.9745706, "latitude": 45.036035}, "selector": "all"}
params_vendors = {"location": {"longitude": 38.9745706, "latitude": 45.036035}, "filters": []}

response = session.post(url=url_vendors, json=params_vendors).json()

# pprint(response)
with open('json_company.json', 'w') as outfile:
    json.dump(response['data']["places_carousels"], outfile, ensure_ascii=False, indent=4)

company = {}

for item in response['data']["places_carousels"]:
    for i in item['payload']['places']:

        actions = i.get('data').get('actions')
        if len(actions) != 0:
            company[i.get('name')] = actions[0].get('payload').get('title')
            # print(f"{i.get('name')} - {actions[0].get('payload').get('title')}")

sale = 0
free = 0

for key, value in company.items():
    if value.startswith('Бесплатная'):
        free += 1
    else:
        sale += 1

print(f'Всего ресторанов - {len(company)}')
print('='*40)
print(f'С бесплатной доставкой - {free * 100 / len(company)} %')
print(f'Доставка со скидкой - {100 - (free * 100 / len(company))} %')

