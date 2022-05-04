from functools import reduce
from typing import Iterable, List

from nya_scraping.apis.api import Api
from nya_scraping.apis.vkapi import VKApi
from nya_scraping.comment import Comment
from nya_scraping.miners.miner import Miner
from nya_scraping.scrapers import VKScraper
from nya_utils.datatools import filter_dataclass_kwargs


class VKMiner(Miner):
    def __init__(self, q, api: VKApi):
        super(VKMiner, self).__init__(q)

        self.api = api
        self.next_from = ''
        self.scraper = VKScraper(api)

    @classmethod
    def create(cls, q, *args, **kwargs):
        return cls(q, VKApi(*args, **kwargs))

    def next(self, count: int = 100) -> Iterable[Comment]:
        if self.next_from is None:
            return

        response = self.api.newsfeed.search(
            q=self.q,
            count=count,
            start_from=self.next_from
        )

        for item in response['items']:
            for comment in self.scraper.get_comments_from_post(item):
                yield comment

        if 'next_from' in response:
            self.next_from = response['next_from']
        else:
            self.next_from = None
