# todo: загружать датасеты (default: config.toml)
import os
from urllib import request

import pandas as pd

from nya_ml_research.config import DATA_PATH, config


def load_RuTweetCorp(positive_link=None, negative_link=None, save_path=None, overwrite=False, concat=False):
    positive_link = positive_link or config['datasets']['sentiment']['RuTweetCorp-positive']['download_link']
    negative_link = negative_link or config['datasets']['sentiment']['RuTweetCorp-negative']['download_link']
    save_path = save_path or DATA_PATH / 'raw'

    if not (positive_path := save_path / 'ru-tweet-corp-positive.csv').is_file() or overwrite:
        request.urlretrieve(positive_link, positive_path)

    if not (negative_path := save_path / 'ru-tweet-corp-negative.csv').is_file() or overwrite:
        request.urlretrieve(negative_link, negative_path)

    if concat:
        read_kwargs = dict(delimiter=';', header=None)
        data = pd.concat((pd.read_csv(positive_path, **read_kwargs), pd.read_csv(negative_path, **read_kwargs)))
        data.to_csv(path := save_path / 'ru-tweet-corp.csv', header=False)

        # os.remove(negative_path)
        # os.remove(positive_path)

        return path
    return positive_path, negative_path


def load_datasets():
    pass


if __name__ == '__main__':
    load_datasets()
