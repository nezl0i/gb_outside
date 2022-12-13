import json
import requests
from dotenv import load_dotenv
import os

load_dotenv()

username = os.getenv('USERNAME')
token = os.getenv('TOKEN')
base_url = 'https://api.github.com/user/repos'

session = requests.Session()
response = session.get(url=base_url, auth=(username, token)).json()

with open('json_repos.json', 'w') as outfile:
    json.dump(response, outfile)

all_repo = {repo["html_url"]: repo['private'] for repo in response}

for key, val in all_repo.items():
    print(f'{key} - {"private" if val else "public"}')
