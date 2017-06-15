"""File Plugin Init
"""
# Public API
from . import _api as api, _model as model, _widget as widget, _error as error, _driver as driver
from ._api import create, get

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


def _init():
    from pytsite import assetman, tpl, lang, http_api
    from . import _http_api_controllers

    # Resources
    lang.register_package(__name__)
    tpl.register_package(__name__)

    assetman.register_package(__name__)
    assetman.t_less(__name__ + '@**/*.less')
    assetman.t_js(__name__ + '@**/*.js')
    assetman.js_module('pytsite-file-widget-files-upload', __name__ + '@js/widget-files-upload')

    # HTTP API handlers
    http_api.handle('POST', 'file', _http_api_controllers.Post(), 'pytsite.file@post')
    http_api.handle('GET', 'file/<uid>', _http_api_controllers.Get(), 'pytsite.file@get')


_init()
