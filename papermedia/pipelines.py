# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from functools import reduce
import pymongo


class MongoPipelineBase(object):
    _mongo_db_name = None
    _mongo_colletion_name = None

    def __init__(self, mongo_host, mongo_post):
        self.mongo_host = mongo_host
        self.mongo_post = mongo_post

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_host=crawler.settings.get('MONGODB_HOST'),
            mongo_post=crawler.settings.get('MONGODB_POST'),
        )

    def open_spider(self, spider):
        assert self._mongo_db_name
        self.client = pymongo.MongoClient(host=self.mongo_host, port=self.mongo_post)
        self.db = self.client[self._mongo_db_name]

    def write_in_mongodb(self, item):
        assert self._mongo_colletion_name
        self.db[self._mongo_colletion_name].insert(dict(item))

    def close_spider(self, spider):
        self.client.close()


class DoubanMoviesPipeline(MongoPipelineBase):
    _mongo_db_name = 'douban'
    _mongo_colletion_name = 'top250'

    def process_item(self, item, spider):
        for key in item:
            item[key] = reduce(lambda acc, elem: acc + elem, item[key])
        self.write_in_mongodb(item)
        return item


class PeopleDailyPipeline(MongoPipelineBase):
    _mongo_db_name = 'papermedia'
    _mongo_colletion_name = 'peopledaily'

    def process_item(self, item, spider):
        for key in item:
            item[key] = reduce(lambda acc, elem: acc + elem, item[key])
        temp = list(map(lambda element: element.strip(), item['news_info'].split('\r\n')))
        if temp:
            item['news_info'] = temp[3] + temp[5] + '版'
        self.write_in_mongodb(item)
        return item
