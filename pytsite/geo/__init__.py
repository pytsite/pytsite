"""Geo Plugin.
"""
__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


def __init():
    """Init wrapper.
    """
    import sys
    from pytsite import assetman
    from pytsite import tpl
    from pytsite import lang
    lang.register_package(__name__)
    assetman.register_package(__name__)
    tpl.register_global('geo', sys.modules[__package__])

__init()


# Public API
from . import _widget as widget, _field as field, _rule as rule
from ._functions import get_map_link
