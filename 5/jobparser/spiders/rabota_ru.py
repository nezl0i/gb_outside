import scrapy
from scrapy.http import HtmlResponse
from items import JobparserItem


def vacancy_parse(response: HtmlResponse):
    company_name = response.xpath("//a[@rel='noopener noreferrer']/text()").get()
    vacancies_name = response.xpath("//h1/text()").get()
    salary = response.xpath("//h3[@itemprop]/text()").getall()
    url = response.url
    _id = response.url
    yield JobparserItem(company_name=company_name, vacancies_name=vacancies_name, salary=salary, url=url, _id=_id)


class RabotaRuSpider(scrapy.Spider):
    name = 'rabota_ru'
    allowed_domains = ['rabota.ru']
    page = 1
    urls = 'https://krasnodar.rabota.ru/?query=Developer%20python&sort=relevance'
    start_urls = [f"{urls}{page}"]

    def parse(self, response):
        page = response.xpath("//a[@class='pagination-list__last-btn']/@href").get()
        if page:
            next_page = RabotaRuSpider.start_urls[0][0:-1] + page[-1]
            yield response.follow(next_page, callback=self.parse)
        links = response.xpath("//h3[@class='vacancy-preview-card__title']/a/@href").getall()
        for link in links:
            # print()
            yield response.follow(link, callback=vacancy_parse)

