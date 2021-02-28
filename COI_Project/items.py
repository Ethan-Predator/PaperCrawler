# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class CoiProjectItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    fileName = scrapy.Field()
    content = scrapy.Field()
    authors = scrapy.Field()
    title = scrapy.Field()
    abstract = scrapy.Field()
    counter = scrapy.Field()
    pass
