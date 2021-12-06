from functools import reduce
from typing import Dict, Any

from ..model import Prediction, Model


fields = [
    'toxic',
    'severe_toxic',
    'obscene',
    'threat',
    'insult',
    'identity_hate',
]


class ToxicPrediction(Prediction):
    def __init__(self, values):
        self._predictions = dict(zip(fields, values))
        self._emoji = '🤬' if reduce(int.__or__, values) else '😀'

    @property
    def predictions(self) -> Dict[str, Any]:
        return self._predictions

    @property
    def emoji(self):
        return self._emoji


class ToxicModel(Model):
    def __init__(self):
        super(Model, self).__init__()

    def call(self, inputs, training=None, mask=None):
        pass

    def get_config(self):
        pass

    def predict(self,
                x,
                batch_size=None,
                verbose=0,
                steps=None,
                callbacks=None,
                max_queue_size=10,
                workers=1,
                use_multiprocessing=False) -> ToxicPrediction:

        from random import randint

        def next_bool():
            return randint(0, 1)

        return ToxicPrediction([next_bool() for i in range(len(fields))])


def load_model() -> ToxicModel:
    return ToxicModel()
