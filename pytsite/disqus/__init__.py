"""Pytsite Disqus Package Init.
"""
# Public API
from . import _widget as widget, _functions as functions

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


def __init():
    """Init wrapper.
    """
    from pytsite import odm, tpl

    odm.register_model('disqus_comment_count', 'pytsite.disqus._model.CommentCount')
    tpl.register_package(__name__)


__init()
