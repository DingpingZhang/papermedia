# -*- coding: utf-8 -*-
import scrapy
import re

from papermedia.items import PeopleDailyItem
from scrapy.http import Request
from scrapy.loader import ItemLoader


class PeopleDailySpider(scrapy.Spider):
    name = "peopledaily"
    # allowed_domains = ["paper.people.com.cn"]
    start_urls = ['http://paper.people.com.cn']

    __root_url = ''
    __re_extract_pure_url = re.compile('^.*?(nbs.+?$)')

    def parse(self, response):
        self.__root_url = response.url.split('nbs')[0]
        links = response.xpath('//a[@id="pageLink"]/@href').extract()
        for next_url in links:
            pure_next_url = self.__re_extract_pure_url.match(next_url).group(1)
            yield Request(self.__root_url + pure_next_url, callback=self.parse_layout)

    def parse_layout(self, response):
        links = response.xpath('//area[@shape="polygon"]/@href').extract()
        for next_url in links:
            yield Request(self.__root_url + next_url, callback=self.parse_news)

    def parse_news(self, response):
        news = response.xpath('//div[@class="text_c"]')
        item_loader = ItemLoader(item=PeopleDailyItem(), selector=news)
        item_loader.add_value('original_link', response.url.__str__())
        item_loader.add_xpath('title', 'h1/text()')
        item_loader.add_xpath('subhead', 'h2/text()')
        item_loader.add_xpath('reporter', 'h4/text()')
        item_loader.add_xpath('news_info', 'div[@class="lai"]/text()')
        item_loader.add_xpath('content', 'div[@class="c_c"]/div[@id="ozoom"]//p/text()')
        return item_loader.load_item()
