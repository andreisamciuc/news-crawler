from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.selector import HtmlXPathSelector

from openpolitics.items import OpenpoliticsItem

import dateutil.parser

class BleskSpider(CrawlSpider):
    name = 'blesk'
    allowed_domains = ['blesk.cz']
    start_urls = ['http://www.blesk.cz']
    cat_re = 'politika|svet'
    rules = (
        # Sites which should be saved
        Rule(
            LinkExtractor(allow='(%s)' % cat_re),
                # deny=('(komplettansicht|weitere|index)$', '/schlagworte/')),
                callback='parse_page',
                follow=True
        ),

        # Sites which should be followed, but not saved
        Rule(LinkExtractor(allow='(%s)' % cat_re, deny='(sport)')),
    )

    def parse_page(self, response):
        hxs = HtmlXPathSelector(response)
        title = hxs.select('//meta[@property="og:title"]/@content').extract_first()
        body = [s.strip() for s in hxs.select('//div[@class="articleBody"]//p//text()').extract()]
        time = hxs.select('//div[@class="dateTime"]//text()').extract_first()

        if body:
            item = OpenpoliticsItem()
            item['title'] = title
            item['text'] = body
            item['url'] = response.url
            # if time:
            # item['date'] = dateutil.parser.parse(time)
            item['time'] = time
            item['i'] = 13

            return item