# -*- coding: utf-8 -*-

import scrapy

class ExampleSpider(scrapy.Spider):
    name = 'example'
    start_urls = ['https://blog.scrapinghub.com']

    def parse(self, response):
        for url in response.css('ul li a::attr("href")').re('.*/category/.*'):
            yield scrapy.Request(response.urljoin(url), self.parse_titles)

    def parse_titles(self, response):
        for post_title in response.css('div.entries > ul > li a::text').extract():
            yield {'title': post_title}