import scrapy


class ArticleSpider(scrapy.spiders.CrawlSpider):
    name = 'Wiki_Articles'
    allowed_domains = ['wikipedia.org']
    start_urls = [
        'https://en.wikipedia.org/wiki/'
    ]

    def parse(self, response):
        url = response.url
        title = response.css('h1::text').extract_first()

        print('URL: {}'.format(url))
        print('Title: {}'.format(title))

        next_page = response.css('li.next a::attr("href)').get()
        if next_page is not None:
            yield response.follow(next_page, self.parse)