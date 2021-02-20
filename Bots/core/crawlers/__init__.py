"""
Base class for Librarian crawlers
"""

from abc import *


class Crawler(metaclass=ABCMeta):

    def __init__(self, name=None, **kwargs):
        if name is not None:
            self.name = name
        elif not getattr(self, 'name', None):
            raise ValueError(f"{type(self).__name__} must have a name")
        self.__dict__.update(kwargs)

    @abstractmethod
    def __call__(self, *args, **kwargs):
        pass
