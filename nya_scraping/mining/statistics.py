from dataclasses import dataclass, field
from operator import mul
from numpy import mean
from typing import List, Dict, Callable

import numpy as np

from nya_utils.datatools import supplier


@dataclass
class StatisticsItem:
    min: float = np.inf
    max: float = -1.
    values: List[float] = field(default_factory=list)
    levels: List[int] = field(default_factory=list)
    coeffs: Dict[int, float] = field(default_factory=supplier({i: 1 for i in range(10)}))

    def append(self, value, level):
        self.min = min(self.min, value)
        self.max = max(self.max, value)
        self.values.append(value)
        self.levels.append(level)

    @property
    def mean(self):
        return mean(self.values)

    @property
    def weighted_mean(self):
        return sum(map(mul, self.values, coeffs := list(map(self.coeffs.get, self.levels)))) / sum(coeffs)

    def __str__(self):
        return f'StatisticsItem(min={self.min}, max={self.max}, mean={self.mean}, weighted_mean={self.weighted_mean})'


@dataclass
class Statistics:
    values: Dict[str, Dict[str, StatisticsItem]] = field(default_factory=dict)
    statistics_item_factory: Callable[[], StatisticsItem] = field(default=StatisticsItem)

    def update(self, model_name: str, predictions: Dict[str, float], level=0):
        self.values.setdefault(model_name, {})

        for label, value in predictions.items(): (
            self
                .values
                .get(model_name)
                .setdefault(label, self.statistics_item_factory())
                .append(value, level)
        )

    def to_dict(self):
        return dict(zip(self.values.keys(), map(str, self.values.values())))
