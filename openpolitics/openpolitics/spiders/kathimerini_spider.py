from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import HtmlXPathSelector

from openpolitics.items import OpenpoliticsItem
import dateutil.parser

class KathiSpider(CrawlSpider):
    name = 'kathi'
    allowed_domains = ['kathimerini.gr']
    start_urls = ['http://www.kathimerini.gr']
    cat_re = 'article'
    rules = (
        # Sites which should be saved
        Rule(
            SgmlLinkExtractor(allow='(%s)' % cat_re),
                # deny=('(komplettansicht|weitere|index)$', '/schlagworte/')),
                callback='parse_page',
                follow=True
        ),

        # Sites which should be followed, but not saved
        Rule(SgmlLinkExtractor(allow='', deny='')),
    )

    def parse_page(self, response):
        hxs = HtmlXPathSelector(response)
        title = hxs.select('//meta[@property="og:title"]/@content').extract_first()
        body = [s.strip() for s in hxs.select('//article[@id="item-article"]//p//text()[not(ancestor::script|ancestor::style|ancestor::noscript)]').extract()]
        time = hxs.select('//article[@id="item-article"]/header/time/@datetime').extract_first()

        if body:
            item = OpenpoliticsItem()
            item['title'] = title
            item['text'] = body
            item['url'] = response.url
            # if time:
            item['date'] = dateutil.parser.parse(time)
            item['i'] = 7

            return item