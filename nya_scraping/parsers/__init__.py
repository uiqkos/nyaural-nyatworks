from typing import Type

from nya_scraping.parsers.manualparser import ManualParser
from nya_scraping.parsers.parser import Parser
from nya_scraping.parsers.vkparser import VKParser

_parsers_by_target = {
    'vk': VKParser,
    'manual': ManualParser,
}


def get(target: str) -> Type[Parser]:
    if target in _parsers_by_target:
        return _parsers_by_target[target]

    return _parsers_by_target['manual']
