# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class DoubanMovieItem(scrapy.Item):
    title = scrapy.Field()
    movie_info = scrapy.Field()
    star = scrapy.Field()
    quote = scrapy.Field()


class PeopleDailyItem(scrapy.Item):
    original_link = scrapy.Field()
    title = scrapy.Field()
    subhead = scrapy.Field()
    reporter = scrapy.Field()
    news_info = scrapy.Field()
    content = scrapy.Field()
