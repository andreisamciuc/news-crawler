from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.selector import HtmlXPathSelector

from openpolitics.items import OpenpoliticsItem
import dateutil.parser

class TaneaSpider(CrawlSpider):
    name = 'tanea'
    allowed_domains = ['tanea.gr']
    start_urls = ['http://www.tanea.gr', 'http://www.tanea.gr/search/?dos=1&area=0&cid=-1&so=1&pt=3&pg=34&author'
                                         '=&words=brexit&fPeriod=29/01/2016&tPeriod=30/01/2017']
    cat_re = 'news'
    rules = [
        # Sites which should be saved
        Rule(
            LinkExtractor(allow=['politics', 'greece', 'world', 'economy'], deny=['/?iid=2', 'articlelist']),
            # deny=('(komplettansicht|weitere|index)$', '/schlagworte/')),
            callback='parse_page',
            follow=True
        ),

        # Sites which should be followed, but not saved
        Rule(LinkExtractor(allow=['http://www.tanea.gr/search/?dos=1&area=0&cid=-1'
                                  '&so=1&pt=3&pg=[0-9]{1-2}&author=&words=brexit&fPeriod=29/01/2016&tPeriod=30/01/2017'],
                           deny=['articlelist'])),
    ]

    def parse_page(self, response):
        hxs = HtmlXPathSelector(response)
        title = hxs.select('//meta[@property="og:title"]/@content').extract_first()
        body = [s.strip() for s in hxs.select('//div[@id="article-content"]//text()').extract()]
        time = hxs.select('//meta[@itemprop="dateCreated"]/@content').extract_first()

        if body and time:
            if time.find('2016') == -1:
                return
            else:
                item = OpenpoliticsItem()
                item['title'] = title
                item['text'] = body
                item['url'] = response.url
                # if time:
                item['date'] = dateutil.parser.parse(time)
                item['i'] = 6

                return item
