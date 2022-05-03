import datetime
from dataclasses import dataclass

from nya_scraping.comment import Comment, Author
from nya_scraping.scrapers.scraper import Scraper

@dataclass  # no args constructor
class ManualScraper(Scraper):
    input_method = 'manual'

    def get_comments(self, inputs, path: int = None, *args: int):
        comment = Comment(
            text=inputs,
            author=Author('', ''),
            date=datetime.datetime.now().strftime('%Y-%m-%d')
        )

        yield comment

    @classmethod
    def can_parse(cls, url) -> bool:
        return True
