import datetime

from nya_scraping.comment import Comment, Author
from nya_scraping.parsers.parser import Parser


class ManualParser(Parser):
    def parse(self, inputs, size: bool = False):
        comment = Comment(
            text=inputs,
            author=Author('', ''),
            date=datetime.datetime.now().strftime('Y-m-d')
        )

        if size:
            return comment, 1

        return comment

    def setup(self, *args, **kwargs) -> 'Parser':
        return self
