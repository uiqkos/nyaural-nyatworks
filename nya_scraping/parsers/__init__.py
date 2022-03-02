from typing import Type

from nya_scraping.parsers.manualparser import ManualParser
from nya_scraping.parsers.parser import Parser
from nya_scraping.parsers.vkparser import VKParser
from nya_scraping.parsers.youtubeparser import YoutubeParser

parsers_by_target = {
    'vk': VKParser,
    'youtube': YoutubeParser,
    'manual': ManualParser,  # last
}


def get(input_method: str) -> Type[Parser]:
    if input_method in parsers_by_target:
        return parsers_by_target[input_method]

    return parsers_by_target['manual']
