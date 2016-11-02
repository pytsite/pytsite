"""Currency HTTP API.
"""
from . import _api

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


def get_list(**kwargs) -> dict:
    """Get currencies list.
    """
    r = {}
    for c in _api.get_all():
        if c.startswith('_'):
            continue

        r[c] = {
            'title': _api.get_title(c),
            'symbol': _api.get_symbol(c),
        }

    return r
