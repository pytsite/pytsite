"""AddThis Plugin Init.
"""
__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


def __init():
    """Init wrapper.
    """
    import sys
    from pytsite import tpl

    tpl.register_package(__name__)
    tpl.register_global('add_this', sys.modules[__name__])


__init()


# Public API
from . import _widget as widget
