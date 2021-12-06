

def identity(x): return x


def compose(*funcs):
    if len(funcs) == 0:
        return identity

    def composed(x):
        for func in funcs:
            x = func(x)

        return x

    return composed
