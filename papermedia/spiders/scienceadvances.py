# -*- coding: utf-8 -*-
import scrapy
from datetime import datetime


class ScienceadvancesSpider(scrapy.Spider):
    name = "scienceadvances"
    # allowed_domains = ["advances.sciencemag.org"]

    def start_requests(self):
        vol = datetime.now().year - 2014
        issue = datetime.now().month - 1
        link = self.start_urls[0] + 'content/{}/{}'.format(vol, issue)
        return link

    def parse(self, response):
        pass
