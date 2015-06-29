"""Tag Package Init
"""
__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


def __init():
    import sys
    from pytsite.core import lang, tpl
    from pytsite import taxonomy
    from . import _model

    lang.register_package(__name__)
    tpl.register_global('tag', sys.modules[__package__])
    taxonomy.register_model('tag', _model.Tag, __name__ + '@tags')

__init()


# Public API
from . import _widget as widget
