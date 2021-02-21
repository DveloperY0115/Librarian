# -*- coding: utf-8 -*-

"""
Default crawler

Instance of this class is used in initialization of Spiders by default.
"""

from Bots.core.crawlers import Crawler
from bs4 import BeautifulSoup


class Default_Crawler(Crawler):

    def __init__(self, name='default_crawler'):
        kwargs = {}
        super().__init__(name, **kwargs)

    def __call__(self, http_response, **kwargs):
        http_headers = http_response.headers
        html = http_response.text
        status = http_response.status_code

        if not http_response.ok:
            super().log("Something went wrong!")
        return http_headers, html, status
