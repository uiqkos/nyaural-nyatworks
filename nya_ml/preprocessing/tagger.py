import re

from pymorphy2 import MorphAnalyzer

from nya_utils.datatools import expand_dict
from nya_utils.functools import get_item_or

UNIVERSAL_POS_TAG_MAPPING = expand_dict({
    ('ADJF', 'ADJS'): 'ADJ',
    ('INFN',): 'VERB',
    ('PRTF', 'PRTS'): 'VERB',
    ('GRND',): 'VERB',
    ('NUMR',): 'NUM',
    ('ADVB',): 'ADV',
    ('NPRO',): 'PRON',
    ('PREP',): 'PART',
    # ('CONJ',): '',
    ('PRCL',): 'PART',
})


class Tagger:
    def __init__(self, replace_e=True, tag_mapping=None):
        self.analyser = MorphAnalyzer(lang='ru', )
        self.replace_e = replace_e
        self.tag_mapping = tag_mapping or {}

    def apply(self, word):
        p = self.analyser.parse(word)[0]

        if p is None:
            return f'{word}_X'

        if p.tag.POS is None:
            return f'{p.normal_form}_X'

        pos = get_item_or(self.tag_mapping, pos := p.tag.POS, default=pos)

        tagged = f'{p.normal_form}_{pos}'

        if self.replace_e:
            tagged = tagged.replace('ё', 'е')

        return tagged

    def unapply(self, tagged: str):
        return tagged.split('_')[0]


_tagger = Tagger(tag_mapping=UNIVERSAL_POS_TAG_MAPPING)


def tag(word: str):
    return _tagger.apply(word)
