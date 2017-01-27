from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.selector import HtmlXPathSelector

from openpolitics.items import OpenpoliticsItem

import dateutil.parser

class JnSpider(CrawlSpider):
    name = 'jn'
    allowed_domains = ['jn.pt']
    start_urls = ['http://www.jn.pt']
    cat_re = 'politica|mundo|economia|justica|nacional'
    rules = (
        # Sites which should be saved
        Rule(
            LinkExtractor(allow=''),
                # deny=('(komplettansicht|weitere|index)$', '/schlagworte/')),
                callback='parse_page',
                follow=True
        ),

        # Sites which should be followed, but not saved
        Rule(LinkExtractor(allow='', deny='')),
    )

    def parse_page(self, response):
        hxs = HtmlXPathSelector(response)
        title = hxs.select('//meta[@property="og:title"]/@content').extract_first()
        body = [s.strip() for s in hxs.select('//div[@class="t-article-content"]//p//text()').extract()]
        time = hxs.select('//meta[@property="article:published_time"]/@content').extract_first()

        if body and time:
            if time.find('2016') == -1:
                return
            else:
                item = OpenpoliticsItem()
                item['title'] = title
                item['text'] = body
                item['url'] = response.url
                # if time:
                item['date'] = dateutil.parser.parse(time)
                # item['time'] = time
                item['i'] = 12
                return item
