# -*- coding: utf-8 -*-
"""
Base class for Librarian crawlers
"""

import logging
import warnings
from abc import *
from typing import Optional


class Crawler(metaclass=ABCMeta):
    """
    Base class for Librarian crawlers. All crawlers must inherit from this.
    This class and all derived ones define pipelines handling
    collected data via HTTP request of spiders.

    Attributes:
        name (str): Name of this instance. Can NOT be None.
        callbacks (list): List of 'callback' instances.
    """

    name: Optional[str] = None

    def __init__(self, name=None, **kwargs):
        """
        Constructor.

        Args:
            name: Name of this instance. Can NOT be None.
            kwargs:
            -
        """
        if name is not None:
            self.name = name
        elif not getattr(self, 'name', None):
            raise ValueError(f"{type(self).__name__} must have a name")
        self.__dict__.update(kwargs)

    @abstractmethod
    def __call__(self, *args, **kwargs):
        pass

    @property
    def logger(self):
        logger = logging.getLogger(self.name)
        return logging.LoggerAdapter(logger, {'spider': self})

    def log(self, message, level=logging.DEBUG, **kwargs):
        self.logger.log(level, message, **kwargs)
