"""CKEditor Plugin Init.
"""
__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


def __init():
    """Init wrapper.
    """
    from pytsite import assetman
    assetman.register_package(__name__)


__init()


# Public API
from . import _widget as widget
