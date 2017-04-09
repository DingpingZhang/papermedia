# -*- coding: utf-8 -*-
import scrapy
from papermedia.items import PeopleDailyItem
from scrapy.http import Request
from scrapy.selector import Selector
import re


class PeopledailySpider(scrapy.Spider):
    name = "peopledaily"
    # allowed_domains = ["paper.people.com.cn"]
    start_urls = ['http://paper.people.com.cn']

    def __init__(self):
        self.__root_url = ''
        self.__re_extract_pure_url = re.compile('^.*?(nbs.+?$)')

    def parse(self, response):
        selector = Selector(response)
        self.__root_url = response.url.split('nbs')[0]
        links = selector.xpath('//a[@id="pageLink"]/@href').extract()
        for next_url in links:
            pure_next_url = self.__re_extract_pure_url.match(next_url).group(1)
            yield Request(self.__root_url + pure_next_url, callback=self.parse_layout)

    def parse_layout(self, response):
        selector = Selector(response)
        links = selector.xpath('//area[@shape="polygon"]/@href').extract()
        for next_url in links:
            yield Request(self.__root_url + next_url, callback=self.parse_news)

    def parse_news(self, response):
        selector = Selector(response)
        news = selector.xpath('//div[@class="text_c"]')
        return PeopleDailyItem(
            original_link=response.url,
            title=self.extract_from(news, 'h1/text()'),
            subhead=self.extract_from(news, 'h2/text()'),
            reporter=self.extract_from(news, 'h4/text()'),
            news_info=self.extract_from(news, 'div[@class="lai"]/text()'),
            content=self.extract_from(news, 'div[@class="c_c"]/div[@id="ozoom"]//p/text()')
        )

    def extract_from(self, selector, xpath_str):
        return self.first_or_default(selector.xpath(xpath_str).extract())

    @staticmethod
    def first_or_default(str_list):
        if str_list:
            if len(str_list) > 1:
                return '<list_sep>'.join(str_list)
            return str_list[0]
        else:
            return ''
