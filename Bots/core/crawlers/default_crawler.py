"""
Default crawler

Instance of this class is used in initialization of Spiders by default.
"""

from Bots.core.crawlers import Crawler


class Default_Crawler(Crawler):

    def __init__(self, name='default_crawler'):
        kwargs = {}
        super().__init__(name, **kwargs)

    def __call__(self, http_response, **kwargs):
        return