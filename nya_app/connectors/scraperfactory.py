from typing import Union, Tuple

from nya_scraping import scrapers
from nya_scraping.comment import Comment
from nya_scraping.scrapers import Scraper


class ScraperFactory:
    def __init__(self, parsers_config: dict):
        self.config = parsers_config

    def create(self, input_method, text, **create_kwargs):
        if input_method == 'auto':
            for input_method_, parser in scrapers.parsers_by_target.items():
                if parser.can_parse(text):
                    input_method = input_method_
                    break

        parser_type = scrapers.get(input_method)

        return parser_type.create(**{
            **self.config[input_method],
            **create_kwargs
        })
