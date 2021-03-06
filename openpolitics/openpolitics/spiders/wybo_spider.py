from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.selector import HtmlXPathSelector

from openpolitics.items import OpenpoliticsItem
import dateutil.parser

class WyboSpider(CrawlSpider):
    name = 'wybo'
    allowed_domains = ['wyborcza.pl']
    start_urls = ['http://wyborcza.pl']
    cat_re = 'html'
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
        title = hxs.select('//h1[@class="art-title"]/text()').extract_first()
        body = [s.strip() for s in hxs.select('//section[@class="art_content"]//p//text()').extract()]
        if not body:
            body = [s.strip() for s in hxs.select('//div[@id="artykul"]//text()').extract()]

        time = hxs.select('//time[@class="art-datetime"]/@datetime').extract_first()
        # if time:
        #     print time

        if body:
            item = OpenpoliticsItem()
            item['title'] = title
            item['text'] = body
            item['url'] = response.url
            # if time:
            # item['date'] = dateutil.parser.parse(time)
            item['time'] = time
            item['i'] = 9

            return item