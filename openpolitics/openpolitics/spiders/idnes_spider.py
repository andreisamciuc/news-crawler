from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.selector import HtmlXPathSelector

from openpolitics.items import OpenpoliticsItem
import dateutil.parser

class IdnesSpider(CrawlSpider):
    name = 'idnes'
    allowed_domains = ['idnes.cz']
    start_urls = ['http://www.idnes.cz']
    rules = (
        # Sites which should be saved
        Rule(
            LinkExtractor(allow='(aspx\?c=A16|aspx\?c=A15)'),
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
        body = [s.strip() for s in hxs.select('//div[@class="text"]//p//text()').extract()]
        time = hxs.select('//meta[@property="article:published_time"]/@content').extract_first()

        if body:
            item = OpenpoliticsItem()
            item['title'] = title
            item['text'] = body
            item['url'] = response.url
            if time:
                item['date'] = dateutil.parser.parse(time)
            item['i'] = 2

            return item