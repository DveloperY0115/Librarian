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


if __name__ == '__main__':
    unittest.main()
