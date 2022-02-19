import datetime

from nya_scraping.comment import Comment, Author
from nya_scraping.parsers.parser import Parser


class ManualParser(Parser):
    def parse(self, inputs) -> Comment:
        return Comment(
            text=inputs,
            author=Author('', ''),
            date=datetime.datetime.now().strftime('Y-m-d')
        )

    def setup(self, *args, **kwargs) -> 'Parser':
        pass
