__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


def dd(var):
    """Debug dump.
    """
    from sys import exit
    print(var)
    exit(-1)


def dict_merge(a: dict, b: dict)->dict:
    """Recursively merges dict's.

    Not just simple a['key'] = b['key'], if both a and bhave a key who's
    value is a dict then dict_merge is called
    on both values and the result stored in the returned dictionary.
    https://www.xormedia.com/recursively-merge-dictionaries-in-python/"""

    if not isinstance(b, dict):
        return b

    from copy import deepcopy

    result = deepcopy(a)

    for k, v in b.items():
        if k in result and isinstance(result[k], dict):
                result[k] = dict_merge(result[k], v)
        else:
            result[k] = deepcopy(v)

    return result