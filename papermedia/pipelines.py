# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from functools import reduce
from pymongo import MongoClient


class MongoPipelineBase(object):
    _mongo_colletion_name = None

    def __init__(self, mongo_uri):
        self.mongo_uri = mongo_uri

    @classmethod
    def from_crawler(cls, crawler):
        return cls(mongo_uri=crawler.settings.get('MONGODB_URI'))

    def open_spider(self, spider):
        assert self._mongo_colletion_name
        self.client = MongoClient(self.mongo_uri)
        self.db = self.client.get_default_database()

    def write_in_mongodb(self, item):
        self.db[self._mongo_colletion_name].insert(dict(item))

    def close_spider(self, spider):
        self.client.close()


class DoubanMoviesPipeline(MongoPipelineBase):
    _mongo_colletion_name = 'top250'

    def process_item(self, item, spider):
        for key in item:
            item[key] = reduce(lambda acc, elem: acc + elem, item[key])
        self.write_in_mongodb(item)
        return item


class PeopleDailyPipeline(MongoPipelineBase):
    _mongo_colletion_name = 'peopledaily'

    def process_item(self, item, spider):
        for key in item:
            item[key] = reduce(lambda acc, elem: acc + elem, item[key])
        temp = list(map(lambda element: element.strip(), item['news_info'].split('\r\n')))
        if temp:
            item['news_info'] = temp[3] + temp[5] + '版'
        self.write_in_mongodb(item)
        return item
