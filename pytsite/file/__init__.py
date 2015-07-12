"""File Plugin Init
"""
__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


def __init():
    from pytsite.core import assetman, router, tpl, lang, odm
    from ._model import File

    odm.register_model('file', File)

    assetman.register_package(__name__)

    router.add_rule(
        '/file/upload/<string:model>',
        'pytsite.file.eps.upload',
        filters=('pytsite.auth.eps.filter_authorize',)
    )

    router.add_rule(
        '/file/download/<string:model>/<string(length=2):p1>/<string(length=2):p2>/<string:filename>',
        'pytsite.file.eps.download',
    )

    lang.register_package(__name__)
    tpl.register_package(__name__)


__init()


# Public API
from . import _functions as functions, _model as model, _widget as widget
