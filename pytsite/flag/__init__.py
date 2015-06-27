"""Flag Plugin Init.
"""
__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


def __init():
    import sys
    from pytsite.core import odm, lang, tpl, assetman
    from . import _model

    lang.register_package(__name__)
    assetman.register_package(__name__)
    tpl.register_package(__name__)
    tpl.register_global('flag', sys.modules[__package__])
    odm.register_model('flag', _model.Flag)


__init()


# Public API
from . import _widget as widget
from ._functions import count
