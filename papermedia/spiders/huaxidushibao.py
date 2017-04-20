# -*- coding: utf-8 -*-
import scrapy

from scrapy.http import Request
from papermedia.items import HuaXiDouShiBaoItem


class HuaXiDuShiBaoSpider(scrapy.Spider):
    name = "huaxidushibao"
    # allowed_domains = ["e.thecover.cn"]
    start_urls = ['http://e.thecover.cn/shtml/index_hxdsb.shtml']

    def __init__(self):
        self.__root_url = 'http://e.thecover.cn/'

    def parse(self, response):
        links = response.xpath('//div[@class="title-wrap mt"]/div/ul/li/a/@href').extract()
        for link in links:
            yield Request(self.__root_url + link, callback=self.parse_news)

    def parse_news(self, response):
        news = response.xpath('//div[@class="detail-box"]')
        title = news.xpath('div[@class="detail-title-box"]')
        return HuaXiDouShiBaoItem(
            subtitle1=self.extract_from(title, 'p[@class="detail-subtitle1"]/text()'),
            title=self.extract_from(title, 'h3/text()'),
            subtitle2=self.extract_from(title, 'p[@class="detail-subtitle2"]/text()'),
            original_link=response.url,
            content=self.extract_from(news, '(p[@class="detail-text"]|h6)/text()')
        )

    def extract_from(self, selector, xpath_str, sep='|'):
        return self.first_or_default(selector.xpath(xpath_str).extract(), sep)

    @staticmethod
    def first_or_default(str_list, sep):
        if str_list:
            return sep.join(map(lambda item: item.strip(), str_list))
        else:
            return ''
