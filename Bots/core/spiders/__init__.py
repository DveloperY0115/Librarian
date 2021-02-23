# -*- coding: utf-8 -*-

"""
Base class for Librarian spiders
"""

import logging
import warnings
import requests
from typing import Optional

from Bots.core.crawlers import Crawler
from Bots.core.crawlers.default_crawler import Default_Crawler


class Spider:
    """
    Abstract base class for Librarian spiders. All spiders must inherit from this.
    This class and all derived ones define procedures sending & receiving requests
    to servers designated by URLs.

    Attributes:
        name (str): Name of this instance. Can NOT be None.
        crawler (object): Crawler defining callbacks.
    """

    name: Optional[str] = None
    custom_settings: Optional[dict] = None

    def __init__(self, name=None, **kwargs):
        """
        Constructor.

        Args:
            name (str): Name of this instance. Can NOT be None.
            kwargs:
                - follow_external_links (boolean): Determine whether spider should follow links to external sites.
                Set to 'False' by default.

        """
        if name is not None:
            self.name = name
        elif not getattr(self, 'name', None):
            raise ValueError(f"{type(self).__name__} must have a name")

        self.__dict__.update(kwargs)

        if not hasattr(self, 'start_urls'):
            self.start_urls = []
        if not hasattr(self, 'crawler'):
            self.crawler = Default_Crawler(self.name + '-crawler')
        elif not issubclass(self.crawler.__class__, Crawler):
            raise TypeError(
                "Cannot initialize instance: Attribute 'crawler' must be an instance of class 'Crawler' or its children"
            )
        if not hasattr(self, 'follow_external_links'):
            self.follow_external_links = False

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

        for url in self.start_urls:
            headers = {'user-agent': self.name}
            try:
                http_response = requests.get(url, headers=headers)
            except requests.exceptions.RequestException:
                self.log('Failed to retrieve HTTP response from the host {}'.format(url))
                http_response = None
            if not http_response:
                yield http_response

    # NOTE: This method is experimental for now. Design decision may change.
    def crawl(self):
        for response in self.initiate_requests():
            yield self.crawler(response)