import json
import requests
from dotenv import load_dotenv
import os
from pprint import pprint

load_dotenv()

base_url = 'https://api.vk.com/method/'
session = requests.Session()

API_ID = os.getenv('API_ID')
TOKEN = os.getenv('TOKEN')
VER = os.getenv('VERSION')

params = {
    'v': VER,
    'extended': 1,
    'access_token': TOKEN
}

response = session.get(f'{base_url}/groups.get', params=params).json()
pprint(response)

with open('json_groups.json', 'w') as outfile:
    json.dump(response, outfile)
