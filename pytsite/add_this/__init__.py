"""AddThis Plugin Init.
"""
# Public API
from . import _widget as widget


__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


def __init():
    """Init wrapper.
    """
    from pytsite import tpl

    tpl.register_package(__name__)


__init()
