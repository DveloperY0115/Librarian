# -*- coding: utf-8 -*-
"""
Callback functions used to process received data
"""

from abc import *
from typing import Optional


class Callback(metaclass=ABCMeta):
    """
    Abstract base class used to build new callbacks

    All callbacks (including user-defined ones) MUST implement method '__call__'.
    All '__call__' method should take Request object as its argument for consistency.

    Attributes:
        - specific_arguments (dict): Options for tweak behaviors of callbacks.
    """

    specific_arguments: Optional[dict] = None

    def __init__(self, *args, **kwargs):
        """
        Constructor.

        @ todo: Give brief explanation about arguments for constructor.
        :param args:
        :param kwargs:
        """
        self.specific_arguments.update(kwargs)
        pass

    @abstractmethod
    def __call__(self, http_response, *args, **kwargs):
        pass


class get_http_header(Callback):

    def __call__(self, http_response, *args, **kwargs):
        return http_response.headers()


class get_html(Callback):

    def __call__(self, http_response, *args, **kwargs):
        return http_response.text()
