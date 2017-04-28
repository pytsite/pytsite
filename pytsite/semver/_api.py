"""PytSite Semantic Versioning Tools Functions
"""
from typing import Iterable as _Iterable, Optional as _Optional
from . import _error

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


def normalize(v: str) -> str:
    """Normalize version string.
    """
    v_list = v.split('.')
    v_len = len(v_list)

    if v_len == 1:
        v_list.extend(['0', '0'])
    elif v_len == 2:
        v_list.append('0')
    elif v_len > 3:
        raise _error.InvalidVersionString("Invalid version string: '{}'.".format(v))

    for v_part in v_list:
        if not v_part.isdigit():
            raise _error.InvalidVersionString("Invalid version string: '{}'.".format(v))

    return '.'.join(v_list)


def to_int(v: str):
    """Convert version string to integer.
    """
    v = normalize(v).split('.')

    return int(v[0]) * 10000 + int(v[1]) * 100 + int(v[2])


def compare(a: str, b: str) -> int:
    """Compare two versions.

    Returns -1 if a < b, 0 if a == b, 1 if a > b
    """
    a_i = to_int(a)
    b_i = to_int(b)

    if a_i < b_i:
        return -1
    elif a_i > b_i:
        return 1
    else:
        return 0


def latest(v: _Iterable) -> _Optional[str]:
    """Get latest version from list of versions.
    """
    try:
        return sorted(v, key=to_int)[-1]
    except IndexError:
        return None
