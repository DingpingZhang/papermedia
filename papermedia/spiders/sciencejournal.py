# -*- coding: utf-8 -*-
import scrapy
from papermedia.items import ScienceJournalItem
from scrapy.http import Request
import re
from scrapy.loader import ItemLoader


class ScienceJournalSpider(scrapy.Spider):
    name = "sciencejournal"
    # allowed_domains = ["science.sciencemag.org"]
    start_urls = ['http://science.sciencemag.org/']

    def __init__(self):
        self.__parse_method_selector = {
            'summary': self.pause_summary,
            'abstract': self.parse_abstract,
            'full': self.pause_full
        }

    def parse(self, response):
        # extract vol and issue.
        edition_info = response.xpath('//div[@class="beta section-title__tagline"]/text()').extract()
        publication_date = edition_info[0]
        vol_issue = edition_info[1]
        subject_nodes = response.xpath('//li[@class="issue-toc-section issue-toc-section-contents"]'
                                       + '/ul[@class="toc-section item-list"]/li')
        for subject_node in subject_nodes:
            subject = subject_node.xpath('./h2').extract()
            item_nodes = subject_node.xpath('./ul[@class="toc-section item-list"]/li')
            for item_node in item_nodes:
                item = ScienceJournalItem(
                    publication_date=publication_date,
                    vol_issue=vol_issue,
                    subject=subject,
                    title=item_node.xpath(
                        './/div[@class="highwire-cite-title media__headline__title"]'
                        + '|.//div[@class="highwire-cite-subtitle media__headline__subtitle"]').extract(),
                    contributors=item_node.xpath(
                        './/span[@class="highwire-citation-authors"]/span/text()').extract()
                )
                meta_dict = {
                    'link_dict': self.get_links(item_node),
                    'science_journal_item': item
                }
                yield self.get_next(meta_dict)

    def pause_summary(self, response):
        item = self.get_science_journal_item(response.meta)
        item['summary'] = response.xpath('//div[@class="section summary"]').extract()
        return self.get_next(response.meta)

    def parse_abstract(self, response):
        item = self.get_science_journal_item(response.meta)
        item['editor_summary'] = response.xpath('//div[@class="section editor-summary"]').extract()
        item['abstract'] = response.xpath('//div[@class="section abstract"]').extract()
        return self.get_next(response.meta)

    def pause_full(self, response):
        item = self.get_science_journal_item(response.meta)
        content = response.xpath('//div[@class="article fulltext-view nonresearch-content"]').extract()
        if content:
            item['content'] = content
            item['pdf_link'] = response.meta['link_dict'].pop('pdf', None)
        return self.get_next(response.meta)

    def get_next(self, meta):
        try:
            method_key, next_link = meta['link_dict'].popitem()
            return Request('http://science.sciencemag.org' + next_link,
                           callback=self.__parse_method_selector[method_key],
                           meta=meta)
        except KeyError:
            return self.get_science_journal_item(meta)

    @staticmethod
    def get_science_journal_item(meta):
        if 'science_journal_item' not in meta:
            meta['science_journal_item'] = ScienceJournalItem()
        return meta['science_journal_item']

    @staticmethod
    def get_links(item_node):
        links = item_node.xpath('.//ul[@class="variant-list media__links"]/li/a/@href').extract()
        result = {}
        for link in links:
            method_key = link.split('.').pop()
            # the information of 'editor-summary' will be obtained from 'abstract'.
            if method_key == 'editor-summary':
                continue
            result[method_key] = link
        return result
