from typing import Iterable

from torch.utils.data import IterableDataset


class Dataset(IterableDataset):
    def __init__(self, iterable):
        self.iterable = iterable

    def __iter__(self):
        return iter(self.iterable)
