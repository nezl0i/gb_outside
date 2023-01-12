import scrapy
from scrapy.http import HtmlResponse
from items import JobparserItem


def vacancy_parse(response: HtmlResponse):
    company_name = response.xpath(
        "//div[contains(@class, 'bloko-column_m-0 bloko-column_l-6')]//span[@data-qa='bloko-header-2']//text()").getall()
    vacancies_name = response.xpath("//h1/text()").get()
    salary = response.xpath("//div[@data-qa='vacancy-salary']//text()").getall()
    url = response.url
    _id = response.url
    yield JobparserItem(company_name=company_name, vacancies_name=vacancies_name, salary=salary, url=url, _id=_id)


class HhRuSpider(scrapy.Spider):
    name = 'hh_ru'
    allowed_domains = ['hh.ru']

    start_urls = [
        'https://krasnodar.hh.ru/vacancies/python-developer']

    def parse(self, response):
        next_page = response.xpath("//a[@data-qa='pager-next']/@href").get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)
        links = response.xpath("//a[@data-qa='serp-item__title']/@href").getall()
        for link in links:
            yield response.follow(link, method='GET', callback=vacancy_parse)
