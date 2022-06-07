from nya_scraping.mining.mining import _model_by_name, create_pool, collect_statistics
from nya_scraping.examples.miner_pool import VK_TOKEN


if __name__ == '__main__':
    key, pool = create_pool(
        host='localhost',
        port=27017,
        db_name='nyadb',
        db_collection='search',
        vk_token=VK_TOKEN,
        vk_api_v='5.131',
        queries='Вышка, ВУЗ, ОГЭ, ЕГЭ, Высшее образование'.split(', '),
        nested_limit=5,
        wrap_comment=True,
        unique=True,
        limit=1000
    )

    pool.start()

    statistics = collect_statistics(
        host='localhost',
        port=27017,
        db_name='nyadb',
        db_collection='search',
        key=key,
        models=_model_by_name.keys()
    )
