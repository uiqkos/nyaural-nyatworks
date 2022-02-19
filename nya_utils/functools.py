from functools import reduce


def identity(x): return x


def _compose2(f1, f2):
    return lambda *args, **kwargs: f2(f1(*args, **kwargs))


def compose(*fs):
    return reduce(_compose2, fs)
