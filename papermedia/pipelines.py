# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from functools import reduce
from pymongo import MongoClient
import re


class MongoPipelineBase(object):
    _mongo_collection_name = None

    def __init__(self, mongo_uri):
        self.mongo_uri = mongo_uri

    @classmethod
    def from_crawler(cls, crawler):
        return cls(mongo_uri=crawler.settings.get('MONGODB_URI'))

    def open_spider(self, spider):
        assert self._mongo_collection_name
        self.client = MongoClient(self.mongo_uri)
        self.db = self.client.get_default_database()

    def write_in_mongodb(self, item):
        self.db[self._mongo_collection_name].insert(dict(item))

    def close_spider(self, spider):
        self.client.close()


class ScienceJournalPipeline(MongoPipelineBase):
    _mongo_collection_name = 'sciencejournal'

    __re_xml_tag = re.compile(r"<.+?>|<.+?/>")
    __re_blank_tab = re.compile(r" {2,}|\t+")

    def process_item(self, item, spider):
        try:
            for key in item:
                if isinstance(item[key], list):
                    item[key] = self.clean_list(item[key])
                elif isinstance(item[key], str):
                    item[key] = self.clean_text(item[key])
        finally:
            return item

    def clean_list(self, list_obj):
        if len(list_obj) == 1:
            return self.clean_text(list_obj.pop())
        elif len(list_obj) > 1:
            return map(self.clean_text, list_obj)

    def clean_text(self, text):
        text = self.clean_xml_text(text)
        text = text.strip()
        text = self.clean_redundant_blank_or_tab(text)
        return text

    def clean_xml_text(self, xml_text):
        if xml_text and isinstance(xml_text, str):
            xml_text = self.__re_xml_tag.sub('', xml_text)
        return xml_text

    def clean_redundant_blank_or_tab(self, text):
        return self.__re_blank_tab.sub(' ', text)


class HuaXiDouShiBaoPipeline(MongoPipelineBase):
    _mongo_collection_name = 'huaxidoushibao'

    def process_item(self, item, spider):
        self.write_in_mongodb(item)
        return item


class DoubanMoviesPipeline(MongoPipelineBase):
    _mongo_collection_name = 'top250'

    def process_item(self, item, spider):
        for key in item:
            item[key] = reduce(lambda acc, elem: acc + elem, item[key])
        self.write_in_mongodb(item)
        return item


class PeopleDailyPipeline(MongoPipelineBase):
    _mongo_collection_name = 'peopledaily'

    def process_item(self, item, spider):
        for key in item:
            item[key] = reduce(lambda acc, elem: acc + elem, item[key])
        temp = list(map(lambda element: element.strip(), item['news_info'].split('\r\n')))
        if temp:
            item['news_info'] = temp[3] + temp[5] + '版'
        self.write_in_mongodb(item)
        return item
