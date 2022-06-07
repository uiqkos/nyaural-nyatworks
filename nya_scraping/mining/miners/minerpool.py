import time
from dataclasses import dataclass, field
from functools import partial
from multiprocessing.pool import ThreadPool
from typing import List, Callable

from nya_scraping.comment import Comment
from nya_scraping.mining.miners.miner import Miner
from nya_scraping.mining.miners.vkminer import VKMiner


def _notify_listeners(listeners, *args, **kwargs):
    for listener in listeners:
        listener(*args, **kwargs)


class MinerPool:
    def __init__(
        self,
        queries: List[str],
        workers: int = 4,
        limit: int = -1,
        sleep: float = 1.,
        on_start: List[Callable] = None,
        on_end: List[Callable[[int], None]] = None,
        on_iteration_end: List[Callable[[Comment, int], None]] = None,
        **miner_kwargs
    ):
        self.queries = queries
        self.workers = workers
        self.limit = limit
        self.sleep = sleep
        self.on_start = on_start or []
        self.on_end = on_end or []
        self.on_iteration_end = on_iteration_end or []

        self.miners = list(map(partial(VKMiner.create, **miner_kwargs), self.queries))

    def start(self):
        _notify_listeners(self.on_start)

        with ThreadPool(self.workers) as pool:
            pool.map(self.next, self.miners)

    def next(self, miner: Miner):
        iteration = 0
        while iteration <= self.limit or self.limit == -1:
            for c in miner.next():
                _notify_listeners(self.on_iteration_end, c, iteration)
                iteration += 1

            time.sleep(self.sleep)

        _notify_listeners(self.on_end, iteration)
