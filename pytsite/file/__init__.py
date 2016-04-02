"""File Plugin Init
"""
# Public API
from . import _api as api, _model as model, _widget as widget
from ._api import create, get, get_by_ref

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


def __init():
    from pytsite import assetman, odm, tpl, lang, router
    from ._model import File

    odm.register_model('file', File)

    assetman.register_package(__name__)

    router.add_rule(
        '/file/upload/<string:model>',
        'pytsite.file.ep.upload',
        filters=('pytsite.auth.ep.filter_authorize',)
    )

    router.add_rule(
        '/file/download/<string:model>/<string(length=2):p1>/<string(length=2):p2>/<string:filename>',
        'pytsite.file.ep.download',
    )

    lang.register_package(__name__)
    tpl.register_package(__name__)


__init()
