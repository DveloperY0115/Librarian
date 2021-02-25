import datetime
import logging
import scrapy

from scrapy.crawler import CrawlerProcess

from Librarian_Wiki.Librarian_Wiki.spiders.article_spider import ArticleSpider

if __name__ == '__main__':
    logging.basicConfig(
        filename='./logs/log-{}.txt'.format(datetime.datetime.now())
    )

    process = CrawlerProcess()
    process.crawl(ArticleSpider)
    process.start()
