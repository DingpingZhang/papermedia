# -*- coding: utf-8 -*-
import scrapy

from datetime import datetime
from papermedia.items import ScienceAdvancesItem
from scrapy.http import Request


class ScienceAdvancesSpider(scrapy.Spider):
    name = "scienceadvances"

    # allowed_domains = ["advances.sciencemag.org"]

    __url_root = 'http://advances.sciencemag.org'

    def start_requests(self):
        vol = datetime.now().year - 2014
        issue = datetime.now().month - 1
        self.__vol_issue = 'VOL {}, ISSUE {}'.format(vol, issue)
        link = self.__url_root + '/content/{}/{}'.format(vol, issue)
        yield self.make_requests_from_url(link)

    def parse(self, response):
        subject_nodes = response.xpath('//li[@class="issue-toc-section issue-toc-section-contents"]'
                                       + '/ul[@class="toc-section item-list"]/li')
        for subject_node in subject_nodes:
            subject = subject_node.xpath('./h2').extract()[0]
            item_nodes = subject_node.xpath('./ul[@class="toc-section item-list"]/li')
            for item_node in item_nodes:
                item = ScienceAdvancesItem(
                    publication_date=item_node.xpath(
                        './/p[@class="highwire-cite-metadata byline"]/time/text()').extract(),
                    vol_issue=self.__vol_issue,
                    subject=subject,
                    title=item_node.xpath(
                        './/div[@class="highwire-cite-title media__headline__title"]'
                        + '|.//div[@class="highwire-cite-subtitle media__headline__subtitle"]').extract(),
                    contributors=item_node.xpath(
                        './/span[@class="highwire-citation-authors"]/span/text()').extract()
                )
                yield Request(self.__url_root + self.get_links(item_node).pop('full'),
                              callback=self.parse_article,
                              meta={'science_journal_item': item})

    def parse_article(self, response):
        item = response.meta['science_journal_item']
        full_text_node = response.xpath('//div[@class="article fulltext-view "]')
        item['abstract'] = full_text_node.xpath('./div[@class="section abstract"]').extract()
        item['keywords'] = full_text_node.xpath('./ul[@class="kwd-group"]/li[@class="kwd"]/text()').extract()
        item['references_and_notes'] = full_text_node.xpath('./div[@class="section ref-list"]'
                                                            + '/ol/li//div[@class="cit-metadata"]').extract()
        item['acknowledgments'] = full_text_node.xpath('./div[@class="ack"]').extract()
        item['content'] = full_text_node.xpath('./*[not(@class="section abstract"'
                                               + ' or @class="kwd-group"'
                                               + ' or @class="section ref-list"'
                                               + ' or @class="ack"'
                                               + ')]').extract()
        return item

    @staticmethod
    def get_links(item_node):
        links = item_node.xpath('.//ul[@class="variant-list media__links"]/li/a/@href').extract()
        result = {}
        for link in links:
            method_key = link.split('.').pop()
            result[method_key] = link
        return result
