from typing import Union, Tuple

from nya_scraping import parsers
from nya_scraping.comment import Comment
from nya_scraping.parsers import Parser


class ParserFactory:
    def __init__(self, parsers_config: dict):
        self.config = parsers_config

    def create(self, input_method, text):
        if input_method == 'auto':
            for input_method_, parser in parsers.parsers_by_target.items():
                if parser.can_parse(text):
                    input_method = input_method_
                    break

        parser_type = parsers.get(input_method)

        return parser_type.create(**self.config[input_method])
