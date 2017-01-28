from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.selector import HtmlXPathSelector

from openpolitics.items import OpenpoliticsItem
import dateutil.parser

class SuedDeutscheSpider(CrawlSpider):
    name = 'sued'
    allowed_domains = ['sueddeutsche.de']
    start_urls = ['http://www.sueddeutsche.de']
    cat_re = 'politik|wirtschaft'
    rules = (
        # Sites which should be saved
        Rule(
            LinkExtractor(allow=['politik', 'wirtschaft']),
                # deny=('(komplettansicht|weitere|index)$', '/schlagworte/')),
                callback='parse_page',
                follow=True
        ),

        # Sites which should be followed, but not saved
        Rule(LinkExtractor(allow=['politik', 'wirtschaft'], deny='')),
    )

    def parse_page(self, response):
        hxs = HtmlXPathSelector(response)
        title = hxs.select('//meta[@property="og:title"]/@content').extract_first()
        body = [s.strip() for s in hxs.select('//section[@class="body"]//p//text()').extract()]
        time = hxs.select('//time[@class="timeformat"]/@datetime').extract_first()

        if body and time:
            if time.find('2016') == -1:
                return
            else:
                item = OpenpoliticsItem()
                item['title'] = title
                item['text'] = body
                item['url'] = response.url
                item['date'] = dateutil.parser.parse(time)
                item['i'] = 4

                return item
