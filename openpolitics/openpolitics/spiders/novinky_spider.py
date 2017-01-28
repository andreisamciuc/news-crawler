from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.selector import HtmlXPathSelector

from openpolitics.items import OpenpoliticsItem
import dateutil.parser

class NovinkySpider(CrawlSpider):
    name = 'novinky'
    allowed_domains = ['novinky.cz']
    start_urls = ['http://www.novinky.cz/archiv?id=8&date=1.01.2016&listType=month',
                  'http://www.novinky.cz/archiv?id=2&date=1.01.2016&listType=month',
                  'http://www.novinky.cz/archiv?id=5&date=1.01.2016&listType=month',
                  'http://www.novinky.cz/archiv?id=8&date=1.02.2016&listType=month',
                  'http://www.novinky.cz/archiv?id=2&date=1.02.2016&listType=month',
                  'http://www.novinky.cz/archiv?id=5&date=1.02.2016&listType=month',
                  'http://www.novinky.cz/archiv?id=8&date=1.03.2016&listType=month',
                  'http://www.novinky.cz/archiv?id=2&date=1.03.2016&listType=month',
                  'http://www.novinky.cz/archiv?id=5&date=1.03.2016&listType=month',
                  'http://www.novinky.cz/archiv?id=8&date=1.04.2016&listType=month',
                  'http://www.novinky.cz/archiv?id=2&date=1.04.2016&listType=month',
                  'http://www.novinky.cz/archiv?id=5&date=1.04.2016&listType=month',
                  'http://www.novinky.cz/archiv?id=8&date=1.05.2016&listType=month',
                  'http://www.novinky.cz/archiv?id=2&date=1.05.2016&listType=month',
                  'http://www.novinky.cz/archiv?id=5&date=1.05.2016&listType=month',
                  'http://www.novinky.cz/archiv?id=8&date=1.06.2016&listType=month',
                  'http://www.novinky.cz/archiv?id=2&date=1.06.2016&listType=month',
                  'http://www.novinky.cz/archiv?id=5&date=1.06.2016&listType=month',
                  'http://www.novinky.cz/archiv?id=8&date=1.07.2016&listType=month',
                  'http://www.novinky.cz/archiv?id=2&date=1.07.2016&listType=month',
                  'http://www.novinky.cz/archiv?id=5&date=1.07.2016&listType=month',
                  'http://www.novinky.cz/archiv?id=8&date=1.08.2016&listType=month',
                  'http://www.novinky.cz/archiv?id=2&date=1.08.2016&listType=month',
                  'http://www.novinky.cz/archiv?id=5&date=1.08.2016&listType=month',
                  'http://www.novinky.cz/archiv?id=8&date=1.09.2016&listType=month',
                  'http://www.novinky.cz/archiv?id=2&date=1.09.2016&listType=month',
                  'http://www.novinky.cz/archiv?id=5&date=1.09.2016&listType=month',
                  'http://www.novinky.cz/archiv?id=8&date=1.10.2016&listType=month',
                  'http://www.novinky.cz/archiv?id=2&date=1.10.2016&listType=month',
                  'http://www.novinky.cz/archiv?id=5&date=1.10.2016&listType=month',
                  'http://www.novinky.cz/archiv?id=8&date=1.11.2016&listType=month',
                  'http://www.novinky.cz/archiv?id=2&date=1.11.2016&listType=month',
                  'http://www.novinky.cz/archiv?id=5&date=1.11.2016&listType=month']
    cat_re = 'ekonomika|domaci|zahranicni'
    rules = (
        # Sites which should be saved
        Rule(
            LinkExtractor(allow=['ekonomika', 'domaci', 'zahranicni']),
                # deny=('(komplettansicht|weitere|index)$', '/schlagworte/')),
                callback='parse_page',
                follow=True
        ),

        # Sites which should be followed, but not saved
        Rule(LinkExtractor(allow=['ekonomika', 'domaci', 'zahranicni', 'archiv'], deny='')),
    )

    def parse_page(self, response):
        hxs = HtmlXPathSelector(response)
        title = hxs.select('//meta[@property="og:title"]/@content').extract_first()
        body = [s.strip() for s in hxs.select('//div[@class="articleBody"]//p//text()').extract()]
        time = hxs.select('//p[@id="articleDate"]/text()').extract_first()

        if body and time:
            if time.find('2016') == -1:
                return
            else:
                item = OpenpoliticsItem()
                item['title'] = title
                item['text'] = body
                item['url'] = response.url
                # if time:
                item['time'] = time
                item['i'] = 3

                return item