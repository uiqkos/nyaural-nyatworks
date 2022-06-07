from pymongo import MongoClient

from nya_app.config import config
from nya_scraping.mining.mining import create_pool


def main(
    host: str,
    port: int,
    db_name: str,
    db_collection: str,
    count: int = 10_000,
):
    """
    Скачивает посты из вк, метка рекламы - marked_as_ads
    """

    mc = MongoClient(host, port)
    db = mc.get_database(db_name)
    coll = db.get_collection(db_collection)

    key, pool = create_pool(
        host, port, db_name, db_collection,
        vk_token=config['scrapers']['vk']['token'],
        vk_api_v=config['scrapers']['vk']['api_v'],
        queries='Образование Новости Природа Музыка Ссылка Реклама Искусство'.split(),
        nested_limit=1,
        wrap_comment=True,
        workers=8,
        limit=count,
        unique=True
    )

    pool.start()


if __name__ == '__main__':
    main(
        host='localhost',
        port=27017,
        db_name='nyadb',
        db_collection='search',
        count=1_000
    )
