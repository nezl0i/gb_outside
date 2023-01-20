import scrapy


class GeekbrainsParserItem(scrapy.Item):
    name = scrapy.Field()
    text = scrapy.Field()
    link = scrapy.Field()
    _id = scrapy.Field()
