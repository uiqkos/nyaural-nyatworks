from abc import ABC, abstractmethod


class Model(ABC):
    @property
    @abstractmethod
    def grad(self):
        raise NotImplementedError()

    @abstractmethod
    def predict(self, *args, **kwargs):
        pass

    @classmethod
    def load(cls, *args, **kwargs):
        return cls()

