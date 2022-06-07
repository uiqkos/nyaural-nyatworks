import json
from argparse import ArgumentParser
from datetime import datetime
from functools import partial
from operator import itemgetter, attrgetter
from typing import List

from pymongo import MongoClient
from tqdm import tqdm
from unpythonic import piped, identity, notf, composel

from nya_app.config import config
from nya_ml import models
from nya_scraping.mining.miners.minerpool import MinerPool
from nya_scraping.mining.statistics import StatisticsItem, Statistics
from nya_utils.datatools import supplier
from nya_utils.functools import sliceargs, compose


def create_pool(
    host: str,
    port: int,
    db_name: str,
    db_collection: str,
    vk_token: str,
    vk_api_v: str,
    queries: List[str],
    nested_limit: int = 5,
    wrap_comment: bool = False,
    workers: int = 4,
    sleep: float = 0.3,
    limit: int = 100,
    unique: bool = False
) -> (str, MinerPool):

    mc = MongoClient(host, port)
    db = mc.get_database(db_name)
    coll = db.get_collection(db_collection)

    if unique:
        hashes = set(map(
            get_hash := composel(
                itemgetter('text'),
                hash,
            ),
            coll.find({})
        ))
        filter_comment = composel(get_hash, notf(hashes.__contains__))

    else:
        hashes = set()
        filter_comment = supplier(True)

    miner_kwargs = dict(
        token=vk_token,
        api_v=vk_api_v,
        nested_limit=nested_limit,
        wrap_comment=wrap_comment
    )

    query_key = str(datetime.now()) + ' -- ' + ', '.join(queries) + ' -- labeled'

    def save(c, _):
        c = c.to_dict()
        if filter_comment(c):
            coll.insert_one({
                'comment': c,
                'key': query_key
            })

    miner_pool = MinerPool(
        queries,
        workers=workers,
        sleep=sleep,
        limit=limit,
        **miner_kwargs
    )

    bar = tqdm()

    miner_pool.on_start.append(partial(print, 'key:', query_key))

    miner_pool.on_iteration_end.append(save)
    miner_pool.on_iteration_end.append(
        sliceargs(composel(attrgetter('text'), hash, hashes.add), take=1))
    miner_pool.on_iteration_end.append(sliceargs(bar.update))

    miner_pool.on_end.append(print)

    return query_key, miner_pool


_model_by_name = {
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
}


def collect_statistics(
    host: str,
    port: int,
    db_name: str,
    db_collection: str,
    key: str,
    models: List[str]
) -> Statistics:
    mc = MongoClient(host, port)
    db = mc.get_database(db_name)
    coll = db.get_collection(db_collection)

    statistics = Statistics(
        statistics_item_factory=partial(StatisticsItem, coeffs={
            0: 1,
            1: 0.5,
            2: 0.1,
            3: 0
        })
    )

    comments = list(coll.find({'key': key}))

    for model_name, model_type in {k: v for k, v in _model_by_name.items() if k in models}.items():
        model = model_type.load()

        list(
            map(
                statistics.update,
                map(
                    compose(
                        itemgetter('comment'),
                        itemgetter('text'),
                        model.predict,
                        {}.setdefault(model_name, {}).update
                    ),
                    comments
                ),
                # map(
                #     compose(
                #         itemgetter('comment'),
                #         itemgetter('level')
                #     ),
                #     comments
                # )
            )
        )

        del model

    print(json.dumps(statistics.to_dict(), ensure_ascii=False, indent=4))


if __name__ == '__main__':
    argument_parser = ArgumentParser()

    argument_parser.add_argument(
        '--host', '-h',
        default='localhost',
        type=str
    )

    argument_parser.add_argument(
        '--port', '-p',
        default=27017,
        type=int
    )

    argument_parser.add_argument(
        '--db-name',
        default='nyadb',
        type=str
    )

    argument_parser.add_argument(
        '--db-collection',
        default='search',
        type=str
    )

    argument_parser.add_argument(
        '--vk-token',
        default=config['scrapers']['vk']['token'],
        type=str
    )

    argument_parser.add_argument(
        '--vk-api-v',
        default='localhost',
        type=str
    )

    argument_parser.add_argument(
        'queries',
        default='',
        type=str
    )

    argument_parser.add_argument(
        '--nested-limit',
        default=5,
        type=int
    )

    argument_parser.add_argument(
        '--sleep',
        default=0.3,
        type=float
    )

    argument_parser.add_argument(
        '--limit',
        default=100,
        type=int
    )

    argument_parser.add_argument(
        '--models',
        default='toxic_skolkovo,sentiment_blanchefort',
        type=int
    )

    args = argument_parser.parse_args()

    key, pool = create_pool(
        host=args.host,
        port=args.port,
        db_name=args.db_name,
        db_collection=args.db_collection,
        vk_token=args.vk_token,
        vk_api_v=args.vk_api_v,
        queries=args.queries.split(','),
        nested_limit=args.nested_limit,
        wrap_comment=False,
        workers=args.workers,
        sleep=args.sleep,
        limit=args.limit,
    )

    pool.start()

    statistics = collect_statistics(
        host=args.host,
        port=args.port,
        db_name=args.db_name,
        db_collection=args.db_collection,
        key=key,
        models=args.models.split(',')
    )
