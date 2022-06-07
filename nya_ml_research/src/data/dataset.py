from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from pathlib import Path
from typing import Union, Callable, Any
from urllib.request import urlretrieve

import kaggle
import pandas as pd
from kaggle import KaggleApi


@dataclass
class DatasetSource(ABC):
    file_name: str
    home_page: str
    open_file: Callable[[Union[Path, str]], Any]

    @abstractmethod
    def load(self, directory: Union[Path, str]):
        pass


@dataclass
class URLDownloadDataSource(DatasetSource):
    url: str

    def load(self, directory: Union[Path, str]):
        path = Path(directory) / self.file_name

        if not path.exists():
            path.parent.mkdir(exist_ok=True, parents=True)
            urlretrieve(self.url, path)

        return self.open_file(path)


@dataclass
class KaggleDatasetSource(DatasetSource):
    owner: str
    dataset_name: str
    _api: KaggleApi = field(default_factory=KaggleApi)

    def __post_init__(self):
        self._api.authenticate()

    def load(self, directory: Union[Path, str]):
        result = self._api.datasets_download(self.owner, self.dataset_name)
        print(result)


RuSentimentDataset = URLDownloadDataSource(
    url='https://github.com/strawberrypie/rusentiment/raw/master/Dataset/rusentiment_random_posts.csv',
    home_page='https://github.com/strawberrypie/rusentiment',
    file_name='rusentiment_random_posts.csv',
    open_file=pd.read_csv,
)
# todo
# KaggleSentimentAnalysisRussian = KaggleDatasetSource(
#
# )

