# -*- coding: utf-8 -*-
"""
Callback functions used to process received data
"""

from abc import *


class Callback(metaclass=ABCMeta):

    def __init__(self):
        pass

    @abstractmethod
    def __call__(self, *args, **kwargs):
        pass
