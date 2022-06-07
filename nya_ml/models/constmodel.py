import random

from nya_ml.models.model import Model


def ConstRandModel(target, labels):
    class _ConstRandModel(Model):
        @property
        def grad(self):
            return dict(zip(self.labels, range(3)))

        def __init__(self):
            self.r = random.uniform(0, 1)
            self.labels = labels

        def predict(self, *args, **kwargs):
            return {label: self.r for label in self.labels}

    return _ConstRandModel


sentiment = ConstRandModel('sentiment', ('positive', 'negative'))
toxic = ConstRandModel('toxic', ('toxic', 'no toxic'))
sarcasm = ConstRandModel('sarcasm', ('sarcasm', 'no sarcasm'))
