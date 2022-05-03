import time
from dataclasses import dataclass, field
from functools import partial
from multiprocessing.pool import ThreadPool
from typing import List, Callable

from nya_scraping.comment import Comment
from nya_scraping.miners.miner import Miner
from nya_scraping.miners.vkminer import VKMiner


def _notify_listeners(listeners, *args, **kwargs):
    for listener in listeners:
        listener(*args, **kwargs)


@dataclass
class MinerPool:
    queries: List[str]
    workers: int = 4
    limit: int = -1
    sleep: float = 1.
    on_start: List[Callable] = field(default_factory=list)
    on_end: List[Callable[[int], None]] = field(default_factory=list)
    on_iteration_end: List[Callable[[Comment, int], None]] = field(default_factory=list)

    def start(self, **miner_kwargs):
        _notify_listeners(self.on_start)

        miners = list(map(partial(VKMiner.create, **miner_kwargs), self.queries))

        pool = ThreadPool(self.workers)

        pool.map(self.next, miners)

        pool.join()
        pool.close()

    def next(self, miner: Miner):
        iteration = 0
        while iteration != self.limit:
            for c in miner.next():
                _notify_listeners(self.on_iteration_end, c, iteration)

            time.sleep(self.sleep)

        _notify_listeners(self.on_end, iteration)
