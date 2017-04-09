# -*- coding: utf-8 -*-
import scrapy

from papermedia.items import DoubanMovieItem
from scrapy.http import Request
from scrapy.selector import Selector


class DoubanmoviesSpider(scrapy.Spider):
    name = "doubanmovies"
    start_urls = ['http://movie.douban.com/top250']

    url = 'http://movie.douban.com/top250'

    def parse(self, response):
        selector = Selector(response)
        movies = selector.xpath('//div[@class="info"]')
        for movie in movies:
            yield DoubanMovieItem(
                title=self.extract_from(movie, 'div[@class="hd"]/a/span/text()', ''),
                movie_info=self.extract_from(movie, 'div[@class="bd"]/p/text()', ''),
                star=self.extract_from(movie, 'div[@class="bd"]/div[@class="star"]/span[@class="rating_num"]/text()'),
                quote=self.extract_from(movie, 'div[@class="bd"]/p[@class="quote"]/span/text()')
            )
        next_link = self.extract_from(selector, '//span[@class="next"]/link/@href')
        if next_link:
            yield Request(self.url + next_link, callback=self.parse)

    def extract_from(self, selector, xpath_str, sep='|'):
        return self.first_or_default(selector.xpath(xpath_str).extract(), sep)

    @staticmethod
    def first_or_default(str_list, sep):
        if str_list:
            return sep.join(map(lambda item: item.strip(), str_list))
        else:
            return ''
