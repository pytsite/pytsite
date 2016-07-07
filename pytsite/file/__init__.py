"""File Plugin Init
"""
# Public API
from . import _api as api, _model as model, _widget as widget, _error as error
from ._api import create, get, get_by_ref

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


def _init():
    from pytsite import assetman, odm, tpl, lang
    from ._model import File

    # ODM model
    odm.register_model('file', File)

    # Resources
    assetman.register_package(__name__)
    lang.register_package(__name__)
    tpl.register_package(__name__)


_init()
