from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.selector import HtmlXPathSelector

from openpolitics.items import OpenpoliticsItem
import dateutil.parser


class RepubblicaSpider(CrawlSpider):
    name = 'repubblica'
    allowed_domains = ['repubblica.it']
    start_urls = ['http://www.repubblica.it/economia/index.html', 'http://www.repubblica.it/']
    rules = (
        # Sites which should be saved
        Rule(
            LinkExtractor(allow=['politica', 'economia'], deny=['miojob', '/2015', '/2014', '/2013', '/2012',
                                                                '/2011', '/2010', '/2009', '/2008',
                                                                '/2007', '/2006', '/2005', '/2004',
                                                                '/2003', '/2002', '/2001', '/2000']),
            # deny=('(komplettansicht|weitere|index)$', '/schlagworte/')),
            callback='parse_page',
            follow=True
        ),

        # Sites which should be followed, but not saved
        Rule(LinkExtractor(allow=['news', 'archivio'], deny=['miojob', '/2015', '/2014', '/2013', '/2012',
                                                                        '/2011', '/2010', '/2009', '/2008',
                                                                        '/2007', '/2006', '/2005', '/2004',
                                                                        '/2003', '/2002', '/2001', '/2000',
                                                                        'filter'])),
    )

    def parse_page(self, response):
        hxs = HtmlXPathSelector(response)
        title = hxs.select(
            '//h1[@itemprop="headline name"]//text()[not(ancestor::script|ancestor::style|ancestor::noscript)]').extract_first()
        if title:
            title = title.strip()
        body = [s.strip() for s in hxs.select(
            '//span[@itemprop="articleBody"]//text()[not(ancestor::script|ancestor::style|ancestor::noscript|ancestor::h1)]').extract()]
        time = hxs.select('//meta[@property="article:published_time"]/@content').extract_first()

        if body and time:
            if time.find('/2016') == -1:
                return
            else:
                item = OpenpoliticsItem()
                item['title'] = title
                item['text'] = body
                item['url'] = response.url
                item['date'] = dateutil.parser.parse(time)
                item['i'] = 1

                return item
