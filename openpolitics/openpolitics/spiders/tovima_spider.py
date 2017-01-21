from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.selector import HtmlXPathSelector

from openpolitics.items import OpenpoliticsItem
import dateutil.parser

class TovimaSpider(CrawlSpider):
    name = 'tovima'
    allowed_domains = ['tovima.gr']
    start_urls = ['http://www.tovima.gr']
    cat_re = 'politics/article|finance/article|world/article'
    rules = (
        # Sites which should be saved
        Rule(
            LinkExtractor(allow='(%s)' % cat_re),
                # deny=('(komplettansicht|weitere|index)$', '/schlagworte/')),
                callback='parse_page',
                follow=True
        ),

        # Sites which should be followed, but not saved
        Rule(LinkExtractor(allow='(%s)' % cat_re, deny='(sports)')),
    )

    def parse_page(self, response):
        hxs = HtmlXPathSelector(response)
        title = hxs.select('//meta[@property="og:title"]/@content').extract_first()
        body = [s.strip() for s in hxs.select('//div[@id="intext_content_tag"]//div//text()').extract()]
        time = hxs.select('//div[@class="article_info"]/text()').extract_first().strip()

        if body:
            item = OpenpoliticsItem()
            item['title'] = title
            item['text'] = body
            item['url'] = response.url
            # if time:
            # item['date'] = dateutil.parser.parse(time)
            item['time'] = time
            item['i'] = 8

            return item