from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import HtmlXPathSelector

from openpolitics.items import OpenpoliticsItem

from simhash import Simhash

class ZeitSpider(CrawlSpider):
    name = 'zeit'
    allowed_domains = ['www.zeit.de']
    start_urls = ['http://www.zeit.de']
    rules = (
        # Sites which should be saved
        Rule(
            SgmlLinkExtractor(
                allow=('/(online|news|politik|wirtschaft|meinung|gesellschaft|kultur|wissen|digital|' \
                       'studium|campus|karriere|lebensart|reisen|mobilitaet|sport|auto)[\/\w-]+$',

                       '/\d{4}/\d{2}/[\w-]+(/seite-\d)?$'),
                deny=('(komplettansicht|weitere|index|magazin)$', '/schlagworte/')),
            callback='parse_page',
            follow=True
        ),

        # Sites which should be followed, but not saved
        Rule(SgmlLinkExtractor(allow='(schlagworte|index)', deny='suche/')),
    )

    def parse_page(self, response):
        hxs = HtmlXPathSelector(response)
        title = hxs.select('//span[@class="article-heading__title"]/text()').extract_first()
        body = hxs.select('//section[@class="article-page"]/p//text()').extract()
        item = OpenpoliticsItem()
        item['title'] = title
        item['body'] = body
        item['url'] = response.url
        # item['simhash'] = str(Simhash(body))
        return item