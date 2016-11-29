from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import HtmlXPathSelector

from openpolitics.items import OpenpoliticsItem
import dateutil.parser

class RepubblicaSpider(CrawlSpider):
    name = 'repubblica'
    allowed_domains = ['repubblica.it']
    start_urls = ['http://www.repubblica.it']
    rules = (
        # Sites which should be saved
        Rule(
            SgmlLinkExtractor(allow='(news)'),
                # deny=('(komplettansicht|weitere|index)$', '/schlagworte/')),
                callback='parse_page',
                follow=True
        ),

        # Sites which should be followed, but not saved
        Rule(SgmlLinkExtractor(allow='', deny='video')),
    )

    def parse_page(self, response):
        hxs = HtmlXPathSelector(response)
        title = hxs.select('//h1[@itemprop="headline name"]//text()[not(ancestor::script|ancestor::style|ancestor::noscript)]').extract_first().strip()
        body = [s.strip() for s in hxs.select('//span[@itemprop="articleBody"]//text()[not(ancestor::script|ancestor::style|ancestor::noscript|ancestor::h1)]').extract()]
        time = hxs.select('//meta[@property="article:published_time"]/@content').extract_first()

        if body:
            item = OpenpoliticsItem()
            item['title'] = title
            item['text'] = body
            item['url'] = response.url
            item['date'] = dateutil.parser.parse(time)
            item['i'] = 1

            return item