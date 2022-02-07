from typing import Type

from ml.src.model import Model
from ml.src.models.always01337 import Always01337
from ml.src.models.constmodel import ConstRandModel
from ml.src.models.randmodel import RandModel
from ml.src.models.blanchefort_rubert_sentiment import RuBertSentiment

# todo remove
_models_by_target = {
    'toxic': {
        '0.1337': Always01337,
        'random': RandModel
    },
    'sentiment': {
        '0.1337': Always01337,
        'blanchefort': RuBertSentiment
    },
    'sarcasm': {
        'const_random': ConstRandModel
    }
}


def get(name, target) -> Type[Model]:
    if name in _models_by_target[target]:
        return _models_by_target[target][name]

    raise Exception()

