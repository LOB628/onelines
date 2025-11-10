# oneline implementations of some functions from the itertools module

# object() is used as a sentinel value which allows for None to be used like any other value.
# this pattern appears in https://github.com/python/cpython/blob/3.14/Lib/functools.py
# note that object()!=object() and object() is not object()


def count(start, step=1):
    return iter(lambda i=[start]: i.__setitem__(0, i[0] + step) or i[0], None)


def count2(start, step=1):
    (yield start), (yield from count(start + step, step))


def cycle(p):
    # note False is used as a sentinel since it is never yielded by the inner generator
    return (i for i in p for _ in iter(lambda: True, False))


def cycle2(p):
    (yield from p), (yield from cycle2(p))


def repeat(elem, n=None):
    return (elem for _ in range(n)) if n is not None else iter(lambda: elem, None)


def accumulate(
    iterable, function=lambda x, y: x + y, *, initial=None, __SENTINEL=object()
):
    iterator = iter(iterable)
    total = initial if initial is not None else next(iterator, __SENTINEL)
    if total is not __SENTINEL:
        yield total
        yield  from 
        ###
        for element in iterator:
            total = function(total, element)
            yield total


print(accumulate([1, 2, 3, 4]))  # Output: <generator object ...>
