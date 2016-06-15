"""PytSite Comments Package Init.
"""
# Public API
from . import _driver as driver, _error as error, _model as model
from ._api import register_driver, get_driver, get_widget, get_comments_count, get_all_comments_count, get_drivers, \
    create_comment, get_comment_statuses


__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


def _init():
    """Init wrapper.
    """
    from pytsite import events
    from . import eh

    events.listen('pytsite.update', eh.pytsite_update)


_init()
