"""PytSite HTTP API Package.
"""
# Public API
from ._controller import Controller
from ._api import handle, url, call, on_pre_request, on_request

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


def _init():
    from pytsite import assetman, router
    from . import _eh

    # HTTP entry point route
    router.handle('/api/<int:version>/<path:endpoint>', 'pytsite.http_api@entry', 'pytsite.http_api@entry',
                  methods='*')

    # JavaScript helpers
    assetman.register_package(__name__)
    assetman.add('pytsite.http_api@js/common.js', True)

    # Event listeners
    router.on_response(_eh.router_response)


_init()
