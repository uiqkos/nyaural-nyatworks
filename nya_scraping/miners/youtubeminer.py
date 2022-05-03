import json
from typing import Iterable

from youtubesearchpython import Comments

from nya_scraping.miners.miner import Miner


class YoutubeMiner(Miner):
    def __init__(self, keywords: Iterable[str], api_key: str, api_v: str, ):
        super(YoutubeMiner, self).__init__(keywords)
        self.comments_search = Comments()

    def save_results(self, results):
        pass

    def parse_page(self, page):
        pass

    def next_page(self, keyword, *args, **kwargs):
        request = self.api.search().list(
            part="snippet",
            maxResults=25,
            q=keyword
        )
        response = request.execute()

        print(json.dumps(response, indent=4, ensure_ascii=False))


