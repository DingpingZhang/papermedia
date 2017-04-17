# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy import Item, Field


class ScienceJournalItem(Item):
    publication_date = Field()
    vol_issue = Field()
    subject = Field()
    title = Field()
    contributors = Field()
    summary = Field()
    editor_summary = Field()
    abstract = Field()
    content = Field()


class HuaXiDouShiBaoItem(Item):
    original_link = Field()
    subtitle1 = Field()
    title = Field()
    subtitle2 = Field()
    reporter = Field()
    news_info = Field()
    content = Field()


class DoubanMovieItem(Item):
    title = Field()
    movie_info = Field()
    star = Field()
    quote = Field()


class PeopleDailyItem(Item):
    original_link = Field()
    title = Field()
    subhead = Field()
    reporter = Field()
    news_info = Field()
    content = Field()
