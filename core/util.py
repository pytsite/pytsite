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


def mk_tmp_file()->str:
    """Creates temporary file.
    """
    from os import path, mkdir
    from tempfile import mkstemp
    from . import reg

    tmp_dir = reg.get('paths.tmp')
    if not tmp_dir:
        raise Exception("Cannot determine temporary directory location.")

    if not path.exists(tmp_dir):
        mkdir(tmp_dir)

    return mkstemp(dir=tmp_dir)


def random_str(size=16, chars='0123456789abcdef'):
    """Generate random string.
    """
    import random
    return ''.join(random.choice(chars) for _ in range(size))


def random_password(size=16):
    """Generate random password.
    """
    chars = 'abcdefghijklmnopqrstuvwxyz0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ!@#$%^&*()_+=-`~|\/.,?><{}[]":;'
    return random_str(size, chars)
