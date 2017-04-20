# -*- coding: utf-8 -*-
import scrapy

from papermedia.items import DoubanMovieItem
from scrapy.http import Request
from scrapy.loader import ItemLoader


class DouBanMoviesSpider(scrapy.Spider):
    name = "doubanmovies"
    start_urls = ['http://movie.douban.com/top250']

    url = 'http://movie.douban.com/top250'

    def parse(self, response):
        movies = response.xpath('//div[@class="info"]')
        for movie in movies:
            item_loader = ItemLoader(item=DoubanMovieItem(), selector=movie)
            item_loader.add_xpath('title', 'div[@class="hd"]/a/span/text()')
            item_loader.add_xpath('movie_info', 'div[@class="bd"]/p/text()')
            item_loader.add_xpath('star', 'div[@class="bd"]/div[@class="star"]/span[@class="rating_num"]/text()')
            item_loader.add_xpath('quote', 'div[@class="bd"]/p[@class="quote"]/span/text()')
            yield item_loader.load_item()

        next_link = response.xpath('//span[@class="next"]/link/@href').extract()
        if next_link:
            yield Request(self.url + next_link[0], callback=self.parse)
