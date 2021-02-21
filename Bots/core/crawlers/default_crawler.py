# -*- coding: utf-8 -*-

"""
Default crawler

Instance of this class is used in initialization of Spiders by default.
"""

from Bots.core.crawlers import Crawler
from bs4 import BeautifulSoup

from Bots.core.crawlers.callbacks import *


class Default_Crawler(Crawler):

    def __init__(self, name='default_crawler'):
        kwargs = {'callbacks': [get_http_header(), get_html()]}
        super().__init__(name, **kwargs)

    def __call__(self, http_response, **kwargs):
        result = {}
        for callback in self.callbacks:
            result[str(callback)] = callback(http_response)
        return result
