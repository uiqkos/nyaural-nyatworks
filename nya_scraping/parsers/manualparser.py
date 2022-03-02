import datetime

from nya_scraping.comment import Comment, Author
from nya_scraping.parsers.parser import Parser


class ManualParser(Parser):
    def parse(self, url, skip: int = 0, take: int = None):
        comment = Comment(
            text=url,
            author=Author('', ''),
            date=datetime.datetime.now().strftime('Y-m-d')
        )

        return comment

    def setup(self, *args, **kwargs) -> 'Parser':
        return self

    @classmethod
    def can_parse(cls, url) -> bool:
        return True
