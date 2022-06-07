import pandas as pd

from nya_ml_research.config import DATA_PATH
from nya_ml_research.src.data.dataset import RuSentimentDataset


def get_rusentiment(path=DATA_PATH / 'raw' / 'sentiment'):
    rusentiment = RuSentimentDataset.load(path)

    rusentiment: pd.DataFrame = rusentiment.loc[
        (rusentiment.label != 'speech') & (rusentiment.label != 'skip')
    ]

    rusentiment['label'] = rusentiment['label'].map({
        'negative': 2,
        'positive': 1,
        'neutral': 0
    })

    return rusentiment


def get_kaggle_news(path=DATA_PATH / 'raw' / 'sentiment' / 'kagglenews.json'):
    kaggle_news = pd.read_json(path)

    kaggle_news.rename(columns={'sentiment': 'label'}, inplace=True)
    kaggle_news.drop(columns=['id'], inplace=True)

    kaggle_news['label'] = kaggle_news['label'].map({
        'negative': 2,
        'positive': 1,
        'neutral': 0
    })

    return kaggle_news


def get_russian_language_toxic_comments(path=DATA_PATH / 'raw' / 'toxic' / 'kaggle_russian_language_toxic_comments.csv'):
    """
    Russian Language Toxic Comments
    Small dataset with labeled comments from 2ch.hk and pikabu.ru

    https://www.kaggle.com/datasets/blackmoon/russian-language-toxic-comments
    """

    ds = pd.read_csv(path)

    ds.rename(columns={'comment': 'text', 'toxic': 'label'}, inplace=True)

    ds['label'] = ds['label'].map(int)

    return ds


def get_toxic_russian_comments(path=DATA_PATH / 'raw' / 'toxic' / 'kaggle_toxic_russian_comments.csv'):
    """
    Toxic Russian Comments
    Labelled comments from the popular Russian social network
    
    https://www.kaggle.com/datasets/alexandersemiletov/toxic-russian-comments
    """

    return pd.read_csv(path)


def fix_toxic_russian_comments(path=DATA_PATH / 'raw' / 'toxic' / 'kaggle_toxic_russian_comments.txt'):
    labels = []
    texts = []

    with open(path, 'r', encoding='utf-8') as f:
        for line in map(str.strip, f.readlines()):
            label, text = line.split(' ', 1)

            if label != '__label__NORMAL':
                labels.append(1)
            else:
                labels.append(0)

            texts.append(text)

    pd.DataFrame({
        'text': texts,
        'label': labels
    }).to_csv(path.with_name(path.name.replace('.txt', '.csv')), index=False)
