"""PytSite HTTP API Package.
"""
# Public API
from ._api import url

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


def _init():
    from pytsite import router, assetman, events, metatag, reg
    from . import ep

    router.add_rule('/api/<int:version>/<package>/<callback>', 'pytsite.http_api@entry')

    assetman.register_package(__name__)
    assetman.add('pytsite.http_api@js/common.js', True)

    api_ver = reg.get('http_api.version', 1)
    events.listen('pytsite.router.dispatch', lambda: metatag.t_set('pytsite-http-api-version', api_ver))


_init()
