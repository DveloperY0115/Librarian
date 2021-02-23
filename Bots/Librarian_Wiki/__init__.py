import scrapy

from scrapy.spiders import CrawlSpider
from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor


class ArticleSpider(CrawlSpider):
    name = 'Wiki_Articles'
    allowed_domains = ['wikipedia.org']
    start_urls = [
        'https://en.wikipedia.org/wiki/Computer'
    ]
    rules = [
        Rule(link_extractor=LinkExtractor(allow='en.wikipedia.org/wiki/((?!:).)*$'),
             callback='parse', follow=False,
             cb_kwargs={'is_article': True}),
        Rule(LinkExtractor(allow='.*'), callback='parse', follow=False,
             cb_kwargs={'is_article': False})
    ]

    def parse(self, response, is_article):
        print(response.url)
        title = response.xpath('//title//text()').get()

        if is_article:
            url = response.url
            text = response.xpath('//div[@id="mw-content-text"]//p/*').getall()
            last_updated = response.xpath('//li[@id="footer-info-lastmod"]//text()').get()
            last_updated = last_updated.replace('This page was last edited on ', '')
            
            print(url)
            print('Title: {}'.format(title))
            print('last updated: {}'.format(last_updated))
            print('Text: {}'.format(text))
        else:
            print('This is not an article: {}'.format(title))
