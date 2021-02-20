# -*- coding: utf-8 -*-

"""
Base class for Librarian spiders
"""

import logging
import warnings
import requests
from typing import Optional

from Bots.core.crawlers.default_crawler import Default_Crawler


class Spider:
    """
    Base class for Librarian spiders. All spiders must inherit from this.
    """

    name: Optional[str] = None
    custom_settings: Optional[dict] = None

    def __init__(self, name=None, **kwargs):
        if name is not None:
            self.name = name
        elif not getattr(self, 'name', None):
            raise ValueError(f"{type(self).__name__} must have a name")
        self.__dict__.update(kwargs)
        if not hasattr(self, 'start_urls'):
            self.start_urls = []
        if not hasattr(self, 'crawler'):
            self.crawler = Default_Crawler(self.name + '-crawler')

    @property
    def logger(self):
        logger = logging.getLogger(self.name)
        return logging.LoggerAdapter(logger, {'spider': self})

    def log(self, message, level=logging.DEBUG, **kwargs):
        self.logger.log(level, message, **kwargs)

    def initiate_requests(self):
        if not self.start_urls and hasattr(self, 'start_url'):
            raise AttributeError(
                "Crawling could not start: Attribute 'start_urls' not found "
                "or empty (but found 'start_url' instead, "
                "did you miss an 's'?)")

        # todo: Replace processing to callbacks defined in Crawler
        for url in self.start_urls:
            headers = {'user-agent': self.name}
            yield requests.get(url, headers=headers)


if __name__ == '__main__':

    my_spidey = Spider('librarian', start_urls=['https://www.gmarket.co.kr'])

    for response in my_spidey.initiate_requests():
        print('----------------\n')
        print('URL: {}'.format(response.url))
        print('Content: \n {}'.format(response.text))
