"""PytSite Comments Package Init.
"""
# Public API
from . import _driver as driver, _error as error, _model as model
from ._api import register_driver, get_driver, get_widget, get_comments_count, get_all_comments_count, get_drivers, \
    create_comment, get_comment_statuses, get_comment_max_depth, get_comment_body_min_length, get_comment, \
    get_comment_body_max_length, get_comments


__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


def _init():
    """Init wrapper.
    """
    from pytsite import events, lang, tpl
    from . import _eh

    events.listen('pytsite.update', _eh.pytsite_update)

    lang.register_package(__name__)
    tpl.register_package(__name__)

_init()
