from nya_utils.functools import identity


def find(iterable, what, key=None):
    key = key or identity

    for item in iterable:
        if key(item) == what:
            return item
