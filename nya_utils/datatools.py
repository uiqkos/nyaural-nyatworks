from dataclasses import fields
from itertools import zip_longest
from operator import attrgetter
from typing import Iterable, Collection

from nya_utils.functools import identity


def filter_dict(include: Collection, dct: dict, return_tuple: bool = False):
    true, false = {}, {}

    for key, value in dct.items():
        if key in include:
            true[key] = value
        else:
            false[key] = value

    if return_tuple:
        return true, false

    return true

    # return dict(filter(lambda item: item[0] in include, dct.items()))


def filter_dataclass_kwargs(dc, dct: dict, return_tuple: bool = False):
    return filter_dict(list(map(attrgetter('name'), fields(dc))), dct, return_tuple=return_tuple)


def expand_single(keys, value):
    return tuple(zip_longest(keys, [value], fillvalue=value))


def expand_dict(dct: dict, seq_type=tuple):
    new = {}
    for key, value in dct.items():
        if isinstance(key, seq_type):
            for key_ in key:
                new[key_] = value

        else:
            new[key] = value

    return new


def cast_arguments(dc):
    if hasattr(dc, '__post_init__'):
        post_init_old = dc.__post_init__
    else:
        post_init_old = identity

    def __post_init__(self):
        post_init_old(self)

        for field in fields(dc):
            value = getattr(self, field.name)
            if value is not None:
                setattr(self, field.name, field.type(value))

    dc.__post_init__ = __post_init__

    return dc


# todo: mb copy
def supplier(o):
    return lambda *args, **kwargs: o

class classproperty(object):
    def __init__(self, fget):
        self.fget = fget
    def __get__(self, owner_self, owner_cls):
        return self.fget(owner_cls)
