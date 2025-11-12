# oneline implementations of some functions from the itertools module

# object() is used as a sentinel value which allows for None to be used like any other value.
# this pattern appears in https://github.com/python/cpython/blob/3.14/Lib/functools.py
# note that object()!=object() and object() is not object()


def count(start, step=1):
    return iter(lambda i=[start]: i.__setitem__(0, i[0] + step) or i[0], None)


def count2(start, step=1):
    (yield start), (yield from count(start + step, step))


def cycle(p):
    # note False is used as a sentinel since it is never yielded by the inner generator to avoid unnecessary use of __SENTINEL = object()
    return (i for i in p for _ in iter(lambda: True, False))


def cycle2(p):
    (yield from p), (yield from cycle2(p))


def repeat(elem, n=None, __SENTINEL=object()):
    return (elem for _ in range(n)) if n is not None else iter(lambda: elem, __SENTINEL)


def accumulate(
    iterable, function=lambda x, y: x + y, *, initial=None, __SENTINEL=object()
):
    (
        (iterator := iter(iterable)),
        (total := initial if initial is not None else next(iterator, __SENTINEL)),
        (
            () if total is __SENTINEL else (yield total),
            (yield from (total := function(total, element) for element in iterator)),
        ),
    )


def batched(p, n):
    (
        (iterator := iter(p)),
        (ret := tuple((elem for _, elem in zip(range(n), iterator)))),
        ((yield ret), (yield from batched(iterator, n))) if ret else None,
    )


def chain(*iterables):
    return (element for p in iterables for element in p)


def chain_from_iterable(iterable):
    return (element for p in iterable for element in p)


def compress(data, selectors):
    return (d for d, s in zip(data, selectors) if s)


def dropwhile(predicate, iterable):
    (
        (iterator := iter(iterable)),
        (yield next(element for element in iterator if not predicate(element))),
        (yield from iterator),
    )


def filterfalse(predicate, iterable):
    return (
        (element for element in iterable if not predicate(element))
        if predicate is not None
        else filterfalse(bool, iterable)
    )


def takewhile(predicate, iterable, __SENTINEL=object()):
    return iter(
        (
            lambda iterator=(
                elem if pred else __SENTINEL
                for elem, pred in zip(iterable, map(predicate, iterable))
            ): next(iterator, __SENTINEL)
        ),
        __SENTINEL,
    )
