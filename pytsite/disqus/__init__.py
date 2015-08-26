"""Pytsite Disqus Package Init.
"""
__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


def __init():
    """Init wrapper.
    """
    import sys
    from pytsite import odm
    from pytsite import tpl

    odm.register_model('disqus_comment_count', 'pytsite.disqus._model.CommentCount')
    tpl.register_package(__name__)
    tpl.register_global('disqus', sys.modules[__package__])

__init()

# Public API
from . import _widget as widget, _functions as functions
