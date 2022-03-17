import re
from abc import abstractmethod, ABC
from typing import Union, Tuple, Iterator, List

from nya_scraping.comment import Comment


class Parser(ABC):
    @classmethod
    def create(cls, *args, **kwargs) -> 'Parser':
        return cls(*args, **kwargs)

    @abstractmethod
    def parse(self, inputs, expand_path: List[str] = None, *args, **kwargs) -> Iterator[Comment]:
        pass
