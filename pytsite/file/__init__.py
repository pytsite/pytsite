"""File Plugin Init
"""
# Public API
from . import _api as api, _model as model, _widget as widget, _error as error
from ._api import create, get, get_by_ref

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


def _init():
    from pytsite import assetman, odm, tpl, lang, events, http_api
    from . import _model, _eh

    # ODM model
    odm.register_model('file', _model.File)

    # Resources
    assetman.register_package(__name__)
    lang.register_package(__name__)
    tpl.register_package(__name__)
    http_api.register_package('file', 'pytsite.file.http_api')

    events.listen('pytsite.setup', _eh.setup)

_init()
