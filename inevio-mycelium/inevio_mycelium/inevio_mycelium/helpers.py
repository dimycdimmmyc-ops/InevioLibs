"""Mycelium helpers."""


def _append(lst, x):
    n = len(lst)
    new_lst = [None] * (n + 1)
    for i in range(n):
        new_lst[i] = lst[i]
    new_lst[n] = x
    return new_lst


def _copy(d):
    new_d = {}
    for k in d:
        new_d[k] = d[k]
    return new_d


def _get(d, key, default=None):
    if not isinstance(d, dict):
        return default
    return d.get(key, default)


def _has(obj, attr):
    return hasattr(obj, attr) and getattr(obj, attr) is not None