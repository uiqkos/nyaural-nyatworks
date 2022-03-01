from abc import abstractmethod, ABC
from typing import Union, Tuple

from nya_scraping.comment import Comment


class Parser(ABC):
    @classmethod
    def create(cls, *args, **kwargs) -> 'Parser':
        return cls(*args, **kwargs)

    @abstractmethod
    def parse(self, inputs, skip: int = 0, take: int = None) -> Union[Comment, Tuple[Comment, int]]:
        pass
