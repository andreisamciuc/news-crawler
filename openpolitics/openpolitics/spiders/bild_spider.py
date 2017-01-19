from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import HtmlXPathSelector

from openpolitics.items import OpenpoliticsItem
import dateutil.parser

class BildSpider(CrawlSpider):
    name = 'bild'
    allowed_domains = ['bild.de']
    start_urls = ['http://www.bild.de']
    rules = (
        # Sites which should be saved
        Rule(
            SgmlLinkExtractor(allow='(news|politik|geld)'),
                # deny=('(komplettansicht|weitere|index)$', '/schlagworte/')),
                callback='parse_page',
                follow=True
        ),

        # Sites which should be followed, but not saved
        Rule(SgmlLinkExtractor(allow='', deny='suche/')),
    )

    def parse_page(self, response):
        hxs = HtmlXPathSelector(response)
        title = hxs.select('//span[@class="headline"]//text()').extract_first().strip()
        body = [s.strip() for s in hxs.select('//div[@class="txt"]/p//text()').extract()]
        time = hxs.select('//div[@class="authors"]//time/@datetime').extract_first()

        if body:
            item = OpenpoliticsItem()
            item['title'] = title
            item['text'] = body
            item['url'] = response.url
            item['date'] = dateutil.parser.parse(time)
            item['i'] = 0

            return item