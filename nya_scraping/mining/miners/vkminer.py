from itertools import islice
from typing import Iterable

import vk

from nya_scraping.comment import Comment, RawComment
from nya_scraping.mining.miners.miner import Miner
from nya_scraping.scrapers import VKScraper


class VKMiner(Miner):
    def __init__(self, q, nested_limit: int = 5, app_id=None, login=None, password=None, token=None, api_v=None, wrap_comment: bool = True):
        super(VKMiner, self).__init__(q)

        self.next_from = ''
        self.nested_limit = nested_limit
        self.wrap_comment = wrap_comment

        if app_id and login and password:
            session = vk.AuthSession(app_id=app_id, user_login=login, user_password=password)
        elif token:
            session = vk.Session(token)
        else:
            session = vk.Session()

        self.api = vk.API(session, v=api_v)
        self.scraper = VKScraper(app_id, login, password, token, api_v, extra=True)

    @classmethod
    def create(cls, *args, **kwargs):
        return cls(*args, **kwargs)

    def next(self, count: int = 100) -> Iterable[Comment]:
        if self.next_from is None:
            return

        response = self.api.newsfeed.search(
            q=self.q,
            count=count,
            start_from=self.next_from
        )

        for item in response['items']:
            post = self.scraper.get_post_from_json(item)
            for comment in islice(self.scraper.get_comments_from_post(post), 0, self.nested_limit):
                yield comment

        if 'next_from' in response:
            self.next_from = response['next_from']
        else:
            self.next_from = None
