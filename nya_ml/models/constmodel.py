import random

from nya_ml.models.model import Model


def ConstRandModel(target):
    class _ConstRandModel(Model):
        def __init__(self):
            self.r = random.uniform(0, 1)
            self.target = target

        def predict(self, *args, **kwargs):
            return {self.target: self.r}

    return _ConstRandModel
