from abc import ABC, abstractmethod


class Model(ABC):
    @abstractmethod
    def predict(self, *args, **kwargs):
        pass

    @classmethod
    def load(cls, *args, **kwargs):
        return cls()

