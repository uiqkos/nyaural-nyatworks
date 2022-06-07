import datetime
import json
import time
from functools import partial
from operator import itemgetter

from pymongo import MongoClient
from tqdm import tqdm

import nya_ml.models as models
from nya_app.config import config
from nya_scraping.mining.miners.minerpool import MinerPool
from nya_scraping.mining.miners.vkminer import VKMiner
from nya_scraping.mining.statistics import Statistics, StatisticsItem
from nya_utils.functools import sliceargs, compose

VK_TOKEN = config['scrapers']['vk']['token']


def make_miner(q, limit: int = -1):
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

    i = 0
    while i <= limit or limit == -1:
        for c in miner.next():
            bar.update()
            coll.insert_one({**c.to_dict(), 'key': query_key})
            i += 1

        else:
            break

    return query_key


def make_pool(queries):
    mc = MongoClient('localhost', 27017)
    db = mc.get_database('nyadb')
    coll = db.get_collection('search')

    miner_kwargs = dict(
        token=VK_TOKEN,
        api_v='5.131',
        nested_limit=5,
        wrap_comment=False
    )

    query_key = str(datetime.datetime.now()) + ' -- ' + ', '.join(queries) + ' -- labeled'

    def save(c, _):
        coll.insert_one({
            'comment': c.to_dict(),
            'key': query_key
        })

    miner_pool = MinerPool(queries, 4, sleep=0.3, limit=-1, **miner_kwargs)
    bar = tqdm()

    miner_pool.on_start.append(partial(print, 'key:', query_key))

    miner_pool.on_iteration_end.append(save)
    miner_pool.on_iteration_end.append(sliceargs(bar.update))

    miner_pool.on_end.append(print)

    miner_pool.start()

    return query_key


def make_statistics(query_key):
    mc = MongoClient('localhost', 27017)
    db = mc.get_database('nyadb')
    coll = db.get_collection('search')

    statistics = Statistics(
        statistics_item_factory=partial(StatisticsItem, coeffs={
            0: 1,
            1: 0.5,
            2: 0.1,
            3: 0
        })
    )

    comments = list(coll.find({'key': query_key}))

    for model_name, model_type in {
        'toxic_skolkovo': (
            models
                .skolkovoInstitute_russian_toxicity_classifier
                .SkolkovoRuToxicityClassifier
        ),
        'toxic_sismetanin': (
            models
                .sismetanin_rubert_toxic
                .SismetaninRuBertToxic
        ),
        'sentiment_blanchefort': (
            models
                .blanchefort_rubert_sentiment
                .BlanchefortRuBertSentiment
        ),
        'sentiment_tatyana': (
            models
                .tatyana_rubert_sentiment
                .TatyanaRuBertSentiment
        ),
    }.items():
        print('Model:', model_type.__name__)
        model = model_type.load('cuda')
        print(' loaded')

        for comment in comments:
            predictions = model.predict(comment['comment']['text'])
            statistics.update(model_type.__name__, predictions)
            comment.setdefault('predictions', {})

            coll.update_one(
                {'_id': comment['_id']},
                {
                    'predictions': {
                        **comment['predictions'],
                        **{model_type.__name__: predictions}
                    }
                }
            )

        # list(
        #     map(
        #         compose(
        #             lambda preds: coll.update_one({'id': }),
        #             partial(statistics.update, model_type.__name__),
        #         ),
        #         map(
        #             compose(
        #                 itemgetter('comment'),
        #                 itemgetter('text'),
        #                 model.predict,
        #             ),
        #             comments
        #         ),
        #         # map(
        #         #     compose(
        #         #         itemgetter('comment'),
        #         #         itemgetter('level')
        #         #     ),
        #         #     comments
        #         # )
        #     )
        # )

        del model

        print(' complete')

    return statistics


if __name__ == '__main__':
    key = make_pool(queries=[
    #     'ЕГЭ',
    #     'ВУЗ',
    #     'Высшее образование',
    #     'ОГЭ',
    #     'высшее профессиональное образование',
        'образование в России',
    #     '',
    #     '',
    #     '',
    #     '',
    ])
    # key = make_miner('образование в России', 1000)
    print(key)

    # stats = make_statistics(key)
    #
    # print(json.dumps(stats.to_dict(), ensure_ascii=False, indent=4))
