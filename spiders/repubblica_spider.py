# -*- coding: utf-8 -*-
import scrapy


class RepubblicaSpider(scrapy.Spider):
    name = "repubblica"
    allowed_domains = ["repubblica.it"]
    start_urls = ['http://repubblica.it/']

    def parse(self, response):
        pass
