# Spider used to crawl Wikipedia articles.

from scrapy.spiders import CrawlSpider
from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor
from Librarian.items import RawWebContent


class ArticleSpider(CrawlSpider):
    name = 'Wiki_Articles'
    allowed_domains = ['wikipedia.org']
    start_urls = [
        'https://en.wikipedia.org/wiki/Computer'
    ]
    rules = [
        Rule(link_extractor=LinkExtractor(allow='en.wikipedia.org/wiki/((?!:).)*$'),
             callback='parse', follow=True)
    ]

    def parse(self, response):
        # self.save_html(response)
        doc = RawWebContent()
        doc['url'] = response.url
        doc['html'] = response.body.decode(response.encoding)
        return doc
