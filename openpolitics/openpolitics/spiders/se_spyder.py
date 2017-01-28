from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.selector import HtmlXPathSelector

from openpolitics.items import OpenpoliticsItem
import dateutil.parser

from simhash import Simhash


class SeSpider(CrawlSpider):
    name = 'se'
    allowed_domains = ['se.pl']
    start_urls = ['http://www.se.pl']
    cat_re = 'polityka|swiat'
    rules = (
        # Sites which should be saved
        Rule(
            LinkExtractor(allow=['polityka', 'swiat']),
            callback='parse_page',
            follow=True
        ),

        # Sites which should be followed, but not saved
        Rule(LinkExtractor(allow=['polityka', 'swiat'])),
    )

    def parse_page(self, response):
        hxs = HtmlXPathSelector(response)
        title = hxs.select('//meta[@property="og:title"]/@content').extract_first()
        body = [s.strip() for s in hxs.select('//div[@class="article__body"]//p//text()').extract()]
        time = hxs.select('//meta[@itemprop="datePublished"]/@content').extract_first()

        if body:
            if time.find('2016') == -1:
                return
            else:
                item = OpenpoliticsItem()
                item['title'] = title
                item['text'] = body
                item['url'] = response.url
                if time:
                    item['date'] = dateutil.parser.parse(time)
                else:
                    item['time'] = hxs.select('//div[@class="akt_bar"]/span/text()').extract()
                # item['time'] = time
                item['i'] = 10

                return item
