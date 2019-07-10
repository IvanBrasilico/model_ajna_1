from scrapy.item import Item, Field
from scrapy.linkextractors import LinkExtractor
from scrapy.selector import Selector
from scrapy.spiders import CrawlSpider, Rule


class myitems(Item):
    referer = Field()
    status = Field()
    response = Field()


class maspider(CrawlSpider):
    name = "brokenlink"
    allowed_domains = ["http://127.0.0.1:8000"]
    start_urls = ['http://http://127.0.0.1:8000']
    handle_httpstatus_list = [404, 410, 301, 500]  # only 200 by default. you can add more status to list
    rules = (
        Rule(LinkExtractor(allow=(''), deny=('pattern_not_to_be_crawled'), unique=('Yes')), callback='parse_my_url',
             follow='True'),
    )


def parse_my_url(self, response):
    sel = Selector(response)
    item = myitems()
    item['referer'] = response.request.headers.get('Referer', None)
    item['status'] = response.status
    item['response'] = response.url
    yield item
