"""
Base class for Librarian spiders
"""

from abc import *

class Spider(metaclass=ABCMeta):

    def __init__(self, args, **kwargs):
        return
    
    @abstractmethod
