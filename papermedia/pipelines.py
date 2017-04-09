# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from scrapy.conf import settings
from papermedia.items import DoubanMovieItem
from re import RegexFlag
import re
import pymongo


class DoubanMoviePipeline(object):
    def __init__(self):
        host = settings['MONGODB_HOST']
        port = settings['MONGODB_PORT']
        db_name = settings['MONGODB_DBNAME']
        client = pymongo.MongoClient(host=host, port=port)
        mongo_db = client[db_name]
        self.mongo_doc = mongo_db[settings['MONGODB_DOCNAME']]

    def process_item(self, item, spider):
        movie_info = dict[item]
        self.mongo_doc.insert(movie_info)
        return item


class PapermediaPipeline(object):
    def process_item(self, item, spider):
        temp = list(map(lambda element: element.strip(), item['news_info'].split('\r\n')))
        if temp:
            item['news_info'] = temp[3] + temp[5] + '版'
        return item
