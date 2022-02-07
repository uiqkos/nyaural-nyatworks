from typing import Type

from ml.src.parsers.parser import Parser
from ml.src.parsers.vkparser import VKParser

_parsers_by_target = {
    'vk': VKParser,
    'manual': Parser,
}


def get(target: str) -> Parser:
    if target in _parsers_by_target:
        return _parsers_by_target[target]()

    return _parsers_by_target['manual']()
