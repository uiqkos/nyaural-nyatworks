import datetime
import time
from collections import Counter
from dataclasses import dataclass, field
from functools import partial

from pymongo import MongoClient
from tqdm import tqdm

import nya_ml.models as models
from nya_app.config import config
from nya_app.connectors.comments import LabeledComment
from nya_app.connectors.modeladapter import ModelAdapter
from nya_scraping.comment import Comment
from nya_scraping.miners.minerpool import MinerPool
from nya_scraping.miners.vkminer import VKMiner
from nya_utils.functools import ignore_args


VK_TOKEN = config['scrapers']['vk']['token']

@dataclass
class Statistics:
    count: int = 0
    toxic_sum: dict[str, float] = field(default_factory=Counter)
    sentiment_sum: dict[str, float] = field(default_factory=Counter)

    toxic_count: dict[str, int] = field(default_factory=Counter)
    sentiment_count: dict[str, int] = field(default_factory=Counter)

    @property
    def toxic_mean(self):
        return {
            k: v / self.count
            for k, v in self.toxic_sum.items()
        }

    @property
    def sentiment_mean(self):
        return {
            k: v / self.count
            for k, v in self.sentiment_sum.items()
        }

    def update(self, comment: LabeledComment):
        return self.update_dict(comment.to_dict())

    def update_dict(self, comment: dict):
        self.count += 1

        max_value, label = 0, ''

        for k, v in comment['predictions']['toxic'].items():
            self.toxic_sum[k] += v

            if max_value < v:
                max_value = v
                label = k

        if label == 'toxic':
            print(comment['text'])
            print()

        self.toxic_count[label] += 1

        max_value, label = 0, ''

        for k, v in comment['predictions']['sentiment'].items():
            self.sentiment_sum[k] += v

            if max_value < v:
                max_value = v
                label = k

        if label == 'negative':
            print(comment['text'])
            print()

        self.sentiment_count[label] += 1


def make_miner():
    q = '#подбор_очька'
    miner = VKMiner.create(
        q=q,
        token=VK_TOKEN,
        api_v='5.131'
    )

    query_key = str(datetime.datetime.now()) + ' -- ' + q
    bar = tqdm()

    mc = MongoClient('localhost', 27017)
    db = mc.get_database('nyadb')
    coll = db.get_collection('search')

    while True:
        for c in miner.next():
            bar.update()
            coll.insert_one({**c.to_dict(), 'key': query_key})

        time.sleep(1)


def make_pool():
    mc = MongoClient('localhost', 27017)
    db = mc.get_database('nyadb')
    coll = db.get_collection('search')

    miner_kwargs = dict(
        token=VK_TOKEN,
        api_v='5.131'
    )

    queries = [
        'ЕГЭ',
        'ВУЗ',
        'Высшее образование',
        'ОГЭ'
    ]

    query_key = str(datetime.datetime.now()) + ' -- ' + ', '.join(queries) + ' -- labeled'

    toxic_model = ModelAdapter(
        models
            .skolkovoInstitute_russian_toxicity_classifier
            .SkolkovoRuToxicityClassifier
            .load()
    )

    sentiment_model = ModelAdapter(
        models
            .blanchefort_rubert_sentiment
            .BlanchefortRuBertSentiment
            .load()
    )

    predictors = {
        'toxic': toxic_model.predict,
        'sentiment': sentiment_model.predict,
    }

    def save(c: Comment, _):
        coll.insert_one({
            **LabeledComment
                .from_predictors(c, predictors)
                .to_dict(),
            'key': query_key
        })

    statistics = Statistics()

    miner_pool = MinerPool(queries, 4, sleep=0.3)
    bar = tqdm()

    miner_pool.on_start.append(partial(print, 'models loaded'))
    miner_pool.on_start.append(partial(print, 'key:', query_key))

    miner_pool.on_iteration_end.append(save)
    miner_pool.on_iteration_end.append(ignore_args(statistics.update))
    miner_pool.on_iteration_end.append(ignore_args(bar.update))

    miner_pool.on_end.append(print)

    miner_pool.start(**miner_kwargs)


def make_statistics():
    mc = MongoClient('localhost', 27017)
    db = mc.get_database('nyadb')
    coll = db.get_collection('search')

    statistics = Statistics()

    for dict_comment in coll.find({}):
        statistics.update_dict(dict_comment)

    print(statistics)
    print('Количество комментариев:', statistics.count)
    print('Средние значения токсичности:', statistics.toxic_mean)
    print('Средние значения эмоциональности:', statistics.sentiment_mean)
    print('Доля токсичных комментариев:', round(statistics.toxic_count['toxic'] / statistics.count, 3))
    print('Доля негативных комментариев:', round(statistics.sentiment_count['negative'] / statistics.count, 3))


if __name__ == '__main__':
    # 634it [06:21,  2.50it/s]
    # make_pool()

    make_statistics()

    # miner = YoutubeMiner(['kotlin'], config['scrapers']['youtube']['key'], config['scrapers']['youtube']['api_v'])
    # miner.start()

    # print('==============================================')
    # print([len(c) for c in miner.next(3)])
    # print('==============================================')
    # print([len(c) for c in miner.next(3)])
