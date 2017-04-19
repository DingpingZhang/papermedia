# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

# from pymongo import MongoClient
import re


class CleanListPipeline(object):
    def process_item(self, item, spider):
        try:
            for key in item:
                if isinstance(item[key], list):
                    item[key] = self.clean_list(item[key])
        finally:
            return item

    def clean_list(self, list_obj):
        if len(list_obj) == 1:
            return list_obj.pop()
        elif len(list_obj) > 1:
            return list_obj
        else:
            return None


class CleanTextPipeline(object):
    __re_xml_tag = re.compile(r"<.+?>|<.+?/>")
    __re_blank_tab = re.compile(r" {2,}|\t+|\n+")

    def process_item(self, item, spider):
        try:
            for key, value in item.items():
                if isinstance(value, str):
                    item[key] = self.clean_text(value)
                elif isinstance(value, list):
                    item[key] = map(self.clean_text, value)
        finally:
            return item

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


# class MongoPipeline(object):
#     def __init__(self, mongo_uri):
#         self.mongo_uri = mongo_uri
#
#     @classmethod
#     def from_crawler(cls, crawler):
#         return cls(mongo_uri=crawler.settings.get('MONGODB_URI'))
#
#     def open_spider(self, spider):
#         assert self._mongo_collection_name
#         self.client = MongoClient(self.mongo_uri)
#         self.db = self.client.get_default_database()
#
#     def process_item(self, item, spider):
#         for key, value in item.items():
#             if isinstance(value, map):
#                 item[key] = list(value)
#         self.db[spider.name].insert(dict(item))
#
#     def close_spider(self, spider):
#         self.client.close()


class PeopleDailyPipeline(object):
    def process_item(self, item, spider):
        temp = list(map(lambda element: element.strip(), item['news_info'].split('\r\n')))
        if temp:
            item['news_info'] = temp[3] + temp[5] + '版'
        return item
