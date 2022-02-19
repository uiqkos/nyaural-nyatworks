import random

from nya_ml.models.model import Model


class ConstRandModel(Model):
    def __init__(self):
        self.r = random.uniform(0, 1)

    def predict(self, *args, **kwargs):
        return {'toxic': self.r}
