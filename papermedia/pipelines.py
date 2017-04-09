# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from scrapy.conf import settings
from papermedia.items import DoubanMovieItem
import pymongo
import re


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
    def __init__(self):
        self.__re_extract_news_info = re.compile(u'(\d{4})年(\d\d?)月(\d\d?)日[\r\n ]*?(\d\d?)[\r\n ]*?')

    def process_item(self, item, spider):
        temp = self.__re_extract_news_info.match(item['news_info'])
        if temp:
            item['news_info'] = '{}-{}-{}-layout:{}'.format(temp.group(1),
                                                            temp.group(2),
                                                            temp.group(3),
                                                            temp.group(4))
        return item
