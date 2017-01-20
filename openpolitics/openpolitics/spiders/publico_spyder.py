from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.selector import HtmlXPathSelector
from scrapy.linkextractors import LinkExtractor
from openpolitics.items import OpenpoliticsItem

import dateutil.parser

class PublicoSpider(CrawlSpider):
    name = 'publico'
    allowed_domains = ['publico.pt']
    start_urls = ['http://www.publico.pt']
    cat_re = 'politica|mundo|economia'
    rules = (
        # Sites which should be saved
        Rule(
            LinkExtractor(allow=''),
                # deny=('(komplettansicht|weitere|index)$', '/schlagworte/')),
                callback='parse_page',
                follow=True
        ),

        # Sites which should be followed, but not saved
        Rule(LinkExtractor(allow='')),
    )

    def parse_page(self, response):
        hxs = HtmlXPathSelector(response)
        title = hxs.select('//meta[@property="og:title"]/@content').extract_first()
        body = [s.strip() for s in hxs.select('//div[@id="story-body"]//p//text()').extract()]
        time = hxs.select('//time[@class="dateline"]/@datetime').extract_first()

        if body:
            item = OpenpoliticsItem()
            item['title'] = title
            item['text'] = body
            item['url'] = response.url
            # if time:
            item['date'] = dateutil.parser.parse(time)
            # item['time'] = time
            item['i'] = 11

            return item