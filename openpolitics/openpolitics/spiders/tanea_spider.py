from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import HtmlXPathSelector

from openpolitics.items import OpenpoliticsItem
import dateutil.parser

class TaneaSpider(CrawlSpider):
    name = 'tanea'
    allowed_domains = ['tanea.gr']
    start_urls = ['http://www.tanea.gr']
    cat_re = 'news'
    rules = (
        # Sites which should be saved
        Rule(
            SgmlLinkExtractor(allow='(%s)' % cat_re),
                # deny=('(komplettansicht|weitere|index)$', '/schlagworte/')),
                callback='parse_page',
                follow=True
        ),

        # Sites which should be followed, but not saved
        Rule(SgmlLinkExtractor(allow='(%s)' % cat_re, deny='(sports)')),
    )

    def parse_page(self, response):
        hxs = HtmlXPathSelector(response)
        title = hxs.select('//meta[@property="og:title"]/@content').extract_first()
        body = [s.strip() for s in hxs.select('//div[@id="article-content"]//text()').extract()]
        time = hxs.select('//meta[@itemprop="dateCreated"]/@content').extract_first()

        if body:
            item = OpenpoliticsItem()
            item['title'] = title
            item['text'] = body
            item['url'] = response.url
            # if time:
            item['date'] = dateutil.parser.parse(time)
            item['i'] = 6

            return item