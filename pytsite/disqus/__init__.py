"""Pytsite Disqus Package Init.
"""
__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

def __init():
    import sys
    from pytsite.core import tpl, odm

    odm.register_model('disqus_comment_count', 'pytsite.disqus._model.CommentCount')
    tpl.register_package(__name__)
    tpl.register_global('disqus', sys.modules[__package__])

__init()

# Public API
from . import _widget as widget, _functions as functions
