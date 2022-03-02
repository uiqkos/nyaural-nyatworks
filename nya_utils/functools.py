from functools import reduce
from operator import itemgetter


def identity(x): return x


def _compose2(f1, f2):
    return lambda *args, **kwargs: f2(f1(*args, **kwargs))


def compose(*fs):
    return reduce(_compose2, fs)


def get_item_or(obj, item, default=None, getter=None, astype=None):
    getter = getter or obj.__getitem__
    astype = astype or (type(default) if default is not None else identity)
    if item in obj:
        return astype(getter(item))
    return default
