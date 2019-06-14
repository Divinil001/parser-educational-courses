# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ExchangeProgramItem(scrapy.Item):
    university_title = scrapy.Field()
    course_title = scrapy.Field()
    semester = scrapy.Field()
    course_credits = scrapy.Field()
    credits_type = scrapy.Field()
    pass
