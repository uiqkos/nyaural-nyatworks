from abc import abstractmethod, ABC
from functools import partial
from multiprocessing import Pool
from typing import List, Iterable

from nya_scraping.comment import Comment


class Miner(ABC):
    def __init__(self, q: str):
        self.q = q
        self.next_page = ''

    @classmethod
    def create(cls, *args, **kwargs):
        return cls(*args, **kwargs)

    @abstractmethod
    def next(self) -> Iterable[Comment]:
        pass

