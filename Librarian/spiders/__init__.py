"""
Base class for Librarian spiders
"""

from abc import *

class Spider(metaclass=ABCMeta):

    def __init__(self, seed_url):
        self.seed_url = seed_url
        return
    
    @abstractmethod
