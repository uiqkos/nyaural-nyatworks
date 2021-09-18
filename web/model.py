import abc
import pickle
from abc import ABC

from tensorflow.keras import Model as KerasModel
from tensorflow.keras.models import load_model, Model


class Serializable(abc.ABC):
    _default_path = None

    @classmethod
    def load(cls):
        return pickle.load(open(cls._default_path, 'rb'))

    def save(self):
        pickle.dump(self, open(self._default_path, 'wb'))


class KerasSerializable(Model, Serializable, abc.ABC):
    _default_path = None

    @classmethod
    def load(cls):
        return load_model(KerasSerializable._default_path)

    def save(self, **kwargs):
        super(KerasSerializable, self).save(KerasSerializable._default_path, **kwargs)


class ToxicModel(KerasSerializable):
    def __init__(self):
        super(KerasSerializable, self).__init__()

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
                use_multiprocessing=False):
        return x
