from abc import abstractmethod, ABC
import pickle
from functools import reduce
from typing import List

from tensorflow.keras.models import load_model, Model as KerasModel


class Prediction:
    fields = []

    @property
    @abstractmethod
    def emoji(self):
        pass

    @property
    @abstractmethod
    def predictions(self):
        pass


class Model(KerasModel, ABC):
    _default_path = None

    @classmethod
    def load(cls):
        return load_model(cls._default_path)

    def save(self, **kwargs):
        super(Model, self).save(Model._default_path, **kwargs)

    @abstractmethod
    def predict(self,
                x,
                batch_size=None,
                verbose=0,
                steps=None,
                callbacks=None,
                max_queue_size=10,
                workers=1,
                use_multiprocessing=False) -> Prediction:
        pass


class Fields:
    fields: List[str] = []

    # todo from json, ...
