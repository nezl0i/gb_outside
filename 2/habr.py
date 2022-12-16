import json
import requests
from lxml import html

url = 'https://habr.com/ru/all'

headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
}

response = requests.get(url, headers=headers)
dom = html.fromstring(response.content)

articles = dom.xpath("//article/div[@class='tm-article-snippet tm-article-snippet']")

article_dict = {}
for article in articles:
    author = article.xpath(
        "div[@class='tm-article-snippet__meta-container']/div[@class='tm-article-snippet__meta']/span[@class='tm-user-info tm-article-snippet__author']/span[@class='tm-user-info__user']/a/text()")[0].strip()
    data_published = article.xpath(
        "div[@class='tm-article-snippet__meta-container']/div[@class='tm-article-snippet__meta']/span[@class='tm-article-snippet__datetime-published']/time/text()")
    theme = article.xpath("h2[@class='tm-article-snippet__title tm-article-snippet__title_h2']/a/span/text()")
    link = article.xpath("h2[@class='tm-article-snippet__title tm-article-snippet__title_h2']/a/@href")

    article_dict[theme[0]] = {
        'author': author,
        'data_published': data_published[0],
        'link': url + link[0]
    }

with open('article_habr.json', 'w', encoding='utf-8') as file:
    json.dump(article_dict, file, ensure_ascii=False, indent=4)
