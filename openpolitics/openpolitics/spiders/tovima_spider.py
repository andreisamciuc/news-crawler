from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.selector import HtmlXPathSelector

from openpolitics.items import OpenpoliticsItem
import dateutil.parser

class TovimaSpider(CrawlSpider):
    name = 'tovima'
    allowed_domains = ['tovima.gr']
    start_urls = ['http://www.tovima.gr/search/?dos=1&cid=-1&sa=0&so=1&regioDate=4&pg=31&author=&words=brexit']
    rules = [
        # Sites which should be saved
        Rule(
            LinkExtractor(allow=['politics/article', 'finance/article', 'world/article'], deny=['&h1=true']),
            # deny=('(komplettansicht|weitere|index)$', '/schlagworte/')),
            callback='parse_page',
            follow=True
        ),

        # Sites which should be followed, but not saved
        Rule(LinkExtractor(allow=['search/?dos=1&cid=-1&sa=0&so=1&reg'
                                  'ioDate=4&pg=[0-9]{1-3}&author=&words=brexit'],
                           deny=['&h1=true'])),
    ]

    def parse_page(self, response):
        hxs = HtmlXPathSelector(response)
        title = hxs.select('//meta[@property="og:title"]/@content').extract_first()
        body = [s.strip() for s in hxs.select('//div[@id="intext_content_tag"]//div//text()').extract()]
        time = hxs.select('//div[@class="article_info"]/text()').extract_first()
        if time:
            time = time.strip()

        if body and time:
            if time.find('2016') == -1:
                return
            else:
                item = OpenpoliticsItem()
                item['title'] = title
                item['text'] = body
                item['url'] = response.url
                # if time:
                # item['date'] = dateutil.parser.parse(time)
                item['time'] = time
                item['i'] = 8

                return item
