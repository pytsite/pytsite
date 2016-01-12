"""PytSite Comments Package Init.
"""
# Public API
from . import _driver as driver, _error as error
from ._driver import Driver
from ._api import register_driver, get_driver, get_widget, get_comments_count, get_all_comments_count, get_drivers

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


def __init():
    """Init wrapper.
    """
    from pytsite import odm
    from . import _model

    odm.register_model('comments_count', _model.CommentsCount)


__init()
