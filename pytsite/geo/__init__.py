"""PytSite Geo Package
"""
# Public API
from . import _widget as widget, _field as field, _rule as rule
from ._functions import get_map_link

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


def __init():
    """Init wrapper.
    """
    import sys
    from pytsite import assetman, lang

    lang.register_package(__name__)
    assetman.register_package(__name__)


__init()
