import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from spiders import wikipedia_spider

process = CrawlerProcess(get_project_settings())

process.crawl(wikipedia_spider.ArticleSpider)
process.start()
