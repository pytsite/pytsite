"""Tag Package Init
"""
__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


def __init():
    from pytsite.core import lang
    from pytsite import taxonomy
    from . import _model

    lang.register_package(__name__)
    taxonomy.manager.register_model('tag', _model.Tag, __name__ + '@tags')

__init()