"""PytSite HTTP API Package.
"""
# Public API
from ._api import handle, url, call, on_pre_request, on_request

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


def _init():
    from pytsite import assetman, router
    from . import _eh, _controllers

    # HTTP entry point route
    router.handle(_controllers.Entry(), '/api/<int:version>/<path:endpoint>', 'pytsite.http_api@entry',
                  methods='*')

    # JavaScript helpers
    assetman.register_package(__name__)
    assetman.t_js(__name__ + '@**')
    assetman.js_module('pytsite-http-api', __name__ + '@pytsite-http-api')

    # Event listeners
    router.on_response(_eh.router_response)


_init()
