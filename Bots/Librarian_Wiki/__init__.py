import scrapy

from scrapy.spiders import CrawlSpider
from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor
from items import Article


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
        article = Article()
        article['url'] = response.url
        article['title'] = response.xpath('//title//text()').get()
        article['text'] = response.xpath('//div[@id="mw-content-text"]//p/*').getall()
        last_updated = response.xpath('//li[@id="footer-info-lastmod"]//text()').get()
        article['last_updated'] = last_updated.replace('This page was last edited on ', '')
        return article
