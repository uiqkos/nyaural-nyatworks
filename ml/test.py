
__gloval__ =12

class A:
    def __init__(self, a, b):
        self.a = a
        self.b = b

        self.some = None

    def f(self, b, *args, **kwargs):
        local_variable = 34224
        print(locals())
        print(globals())


A(1, 2).f(3, [1, 2], 'lol', b2=11)

