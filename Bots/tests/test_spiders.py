import unittest

from Bots.core.crawlers.default_crawler import Default_Crawler
from Bots.core.crawlers import Crawler
from Bots.core.spiders import Spider


class TestSpiderConstructor(unittest.TestCase):

    # Generating Spider without naming it is not allowed.
    def test_empty_name(self):
        with self.assertRaises(ValueError):
            spider = Spider()   # name is empty

    # Construction without specifying crawler should make one for it.
    def test_default_crawler_gen(self):
        spider = Spider('test')
        self.assertEqual(spider.crawler.name, 'test-crawler')
        self.assertTrue(isinstance(spider.crawler, Default_Crawler))

    # Type of passed crawler object must be checked.
    def test_invalid_crawler(self):
        invalid_crawler = str('Hello')
        with self.assertRaises(TypeError):
            spider = Spider('test', crawler=invalid_crawler)


class TestSpiderWithDefaultCrawler(unittest.TestCase):

    # todo: refine this test
    def test_send_http_request(self):
        test_url = 'http://www.google.com'
        spider = Spider('test', start_urls=[test_url])
        header, html, stat_code = spider.initiate_requests()
        print(header)
        print(html)
        print(stat_code)


if __name__ == '__main__':
    unittest.main()
