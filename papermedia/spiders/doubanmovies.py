# -*- coding: utf-8 -*-
import scrapy

from papermedia.items import DoubanMovieItem
from scrapy.http import Request
from scrapy.selector import Selector


class DoubanmoviesSpider(scrapy.Spider):
    name = "doubanmovies"
    # allowed_domains = ["movie.douban.com/top250"]
    start_urls = ['http://movie.douban.com/top250']

    url = 'http://movie.douban.com/top250'

    def parse(self, response):
        item = DoubanMovieItem()
        selector = Selector(response)
        movies = selector.xpath('//div[@class="info"]')
        for movie in movies:
            title = movie.xpath('div[@class="hd"]/a/span/text()').extract()
            full_title = ''.join(title)
            movie_info = movie.xpath('div[@class="bd"]/p/text()').extract()
            star = movie.xpath('div[@class="bd"]/div[@class="star"]/span[@class="rating_num"]/text()').extract()
            quote = movie.xpath('div[@class="bd"]/p[@class="quote"]/span/text()').extract()
            if quote:
                quote = quote[0]
            else:
                quote = ''
            item['title'] = full_title
            item['movie_info'] = ';'.join(movie_info)
            item['star'] = star
            item['quote'] = quote
            yield item

        next_link = selector.xpath('//span[@class="next"]/link/@href').extract()
        if next_link:
            next_link = next_link[0]
            yield Request(self.url + next_link, callback=self.parse)


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
