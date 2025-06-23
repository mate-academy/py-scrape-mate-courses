# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class CourseParserItem(scrapy.Item):
    name = scrapy.Field()
    short_description = scrapy.Field()
    duration = scrapy.Field()
    modules = scrapy.Field()
    topics = scrapy.Field()
