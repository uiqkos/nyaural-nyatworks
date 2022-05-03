import re
from abc import abstractmethod, ABC
from typing import Union, Tuple, Iterator, List, Iterable

from nya_scraping.comment import Comment


class Scraper(ABC):
    input_method = None

    @abstractmethod
    def get_comments(self, inputs, path: List[str] = None, *args, **kwargs) -> Iterable[Comment]:
        pass

    @abstractmethod
    def can_parse(self, inputs) -> bool:
        pass
