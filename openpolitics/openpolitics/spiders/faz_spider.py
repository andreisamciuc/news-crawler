from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.selector import HtmlXPathSelector

from openpolitics.items import OpenpoliticsItem
import dateutil.parser

class FAZSpider(CrawlSpider):
    name = 'faz'
    allowed_domains = ['faz.net']
    start_urls = ['http://www.faz.net']
    cat_re = 'politik|wirtschaft|finanzen'
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
        title = hxs.select('//meta[@property="og:title"]/@content').extract_first()
        body = [s.strip() for s in hxs.select('//div[@class="FAZArtikelText"]//p//text()').extract()]
        time = hxs.select('//span[@class="Datum"]/@content').extract_first()

        if body:
            if time.find('2016') == -1:
                print time
            else:
                item = OpenpoliticsItem()
                item['title'] = title
                item['text'] = body
                item['url'] = response.url
                # if time:
                item['time'] = time
                item['i'] = 5

                return item