from abc import abstractmethod, ABC

from nya_scraping.comment import Comment


class Parser(ABC):
    @classmethod
    def create(cls) -> 'Parser':
        return cls()

    @abstractmethod
    def parse(self, inputs) -> Comment:
        pass

    @abstractmethod
    def setup(self, *args, **kwargs) -> 'Parser':
        pass

