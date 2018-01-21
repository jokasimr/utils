from functools import wraps
from itertools import chain


def cache(args_dict, max_size=128):
    '''
    Decorator to make a function cache its return values for later calls
    '''
    def decorator(fun):

        @wraps(fun)
        def cached_func(*args, **kwargs):
            argument_tuple = (tuple(args), tuple(sorted(kwargs.items())))
            if argument_tuple in args_dict:
                return args_dict[argument_tuple]
            else:
                return_value = fun(*args, **kwargs)
                if max_size >= len(args_dict):
                    args_dict[argument_tuple] = return_value
                return return_value

        return cached_func

    return decorator


def flatten(iterable):
    '''
    Takes a iterable of nested iterables and yields each 'atom' in
    the nested structure. An atom is a non-iterable or a string.
    '''
    if not hasattr(iterable, '__iter__')  or type(iterable) == str:
        yield iterable
        return
    iterable = iter(iterable)

    while 1:
        try:
            item = next(iterable)
        except StopIteration:
            break
        try:
            if type(item) == str:
                yield item
            else:
                data = iter(item)
                iterable = chain(data, iterable)
        except TypeError:
            yield item


import re


def split(delimiter, string):
    '''Splits the string on the delimiters.

    Like the built-in *split* method, but with extra power.
    Args:
        delimiter : Regex of characters to split around.
        string    : The string to split

    Returns:
        iterable of the pieces
    '''
    regex = r'[^{}]+'.format(delimiter)
    yield from (m.group(0) for m in re.finditer(regex, string))


def split_rows(rows):
    '''First splits the string on rows,
       then the rows on whitespace.'''
    rows = rows.split('\n')
    return [[*split(r'\s', row)]
            for row in rows]


from itertools import zip_longest


def chunks(iterable, n, fillvalue=None):
    '''Take the items from the iterable in chunks of n.
       If the values run out 'fillvalue' will be used instead.'''
    it = iter(iterable)
    if fillvalue is None:
        return zip_longest(*(it for i in range(n)))
    return zip_longest(*(it for i in range(n)), fillvalue=fillvalue)


from collections import deque


def neighbors(iterable, n):
    deq = deque([], maxlen=n)
    for item in iterable:
        deq.append(item)
        if len(deq) < n:
            continue
        yield tuple(deq)


def unzip(mapping):
    return zip(*mapping)


def GroupDict(mapping):
    '''Takes a mapping, ((key, value), (key, value) ... )
       and returns a dict with the values grouped by key.

    Returns:
        dict( key : set(value1, value2 ... ) )
    '''
    dictionary = dict()
    for k, v in mapping:
        if k in dictionary:
            dictionary[k].add(v)
            continue
        dictionary[k] = {v}
    return dictionary


from itertools import tee


def teemap(key, iterable):
    it, itp = tee(iterable)
    return map(key, it), itp


def group(iterable, key):
    return GroupDict(zip(*teemap(key, iterable)))


import numpy as np


def linear_interp(time, values, errors, n=100):
    '''Interpolates values between given datapoints'''
    if not n:
        n = int(time[-1] - time[0])
    new_time = np.linspace(time[0], time[-1], n)
    new_vals = np.interp(new_time, time, values)
    new_errs = np.interp(new_time, time, errors)
    return new_time, new_vals, new_errs


def moving_average(a, n=3):
    ret = np.cumsum(a, dtype=float)
    ret[n:] = ret[n:] - ret[:-n]
    return ret[n - 1:] / n


def laplacian2d(Z, dx):
    '''
    Argument should be a 2d numpy array,
    returned array has dimensions (n-1)x(k-1)
    '''
    Ztop = Z[0:-2, 1:-1]
    Zleft = Z[1:-1, 0:-2]
    Zbottom = Z[2:, 1:-1]
    Zright = Z[1:-1, 2:]
    Zcenter = Z[1:-1, 1:-1]
    return (Ztop + Zleft + Zbottom + Zright - 4 * Zcenter) / dx**2


from random import random


def sign(a):
    if a == 0:
        return 1
    return a/abs(a)


def itersolve(func, expected, start=0,
              step=1, tolerance=0.1, max_iterations=100):
    cnt = 1
    oldx = start
    x = start

    olddiff = expected-func(x)
    oldsgn = sign(olddiff)

    x += step
    diff = expected-func(x)
    sgn = sign(diff)

    while abs(diff) > tolerance:

        if abs(diff) > abs(olddiff):

            if sgn == oldsgn:
                step = -step
            else:
                step = step/2

            x = oldx

        else:
            if sgn == oldsgn:
                pass
            else:
                step = -step/2

            oldx = x
            olddiff = diff
            oldsgn = sgn

        x += step
        diff = expected - func(x)
        sgn = sign(diff)

        cnt += 1
        if cnt >= max_iterations:
            break

    return x, func(x), cnt


from math import log10, floor


def solve(func, expected, interval=(-10, 10), n=100, tolerance=0.1, give_all=False):
    ''' Tries itersolve for the expected value on n different places along
        the given interval.

        Returns: The successful return values, x and y sorted from best to worst.

        Example:
            f = lambda x: x**2 + 1
            solve(f, 3, tolerance=0.01, interval=(-10, 10))'''
    start, stop = interval
    step = abs(stop-start)/n
    results = []
    for k in range(n):
        x, y, c = itersolve(
                func,
                expected,
                start=start+step*k,
                step=step*random()+step/2,
                tolerance=tolerance)

        if abs(expected-y) < tolerance:
            results.append((x, y))

    if give_all:
        return sorted(results, key=lambda v: abs(expected-v[1]))

    exponent = -log10(tolerance)
    if not exponent == floor(exponent):
        exponent = floor(exponent+1)
    print(int(exponent))
    result = GroupDict(map(lambda v: (round(v[0], int(exponent)), v), results))

    def aggregate(res):
        return sorted(res, key=lambda x: abs(expected-x[1]))[0]

    for res in result:
        result[res] = aggregate(result[res])
    return result.values()
