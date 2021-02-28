# Spider used to crawl Wikipedia articles.

from scrapy.spiders import CrawlSpider
from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor
from Librarian.items import Article


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
        article = Article()
        article['url'] = response.url
        article['title'] = response.xpath('//title//text()').extract_first()
        article['text'] = self.get_first_paragraph(response)
        article['last_updated'] = response.xpath('//li[@id="footer-info-lastmod"]//text()').extract_first()
        return article

    def get_first_paragraph(self, response):
        text = response.xpath('//div[@id="mw-content-text"]//p[not(@class="mw-empty-elt")]').extract_first()
        return text

    def save_html(self, response):
        html = response.body.decode(response.encoding)
        title = response.xpath('//title//text()').extract_first().replace(' ', '')
        filename = './Data/html/' + title + ".html"
        with open(filename, 'w', encoding=response.encoding) as f:
            f.write(html)
        f.close()

