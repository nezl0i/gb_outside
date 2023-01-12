import scrapy


class JobparserItem(scrapy.Item):
    # define the fields for your item here like:
    company_name = scrapy.Field()
    vacancies_name = scrapy.Field()
    salary = scrapy.Field()
    url = scrapy.Field()
    _id = scrapy.Field()
