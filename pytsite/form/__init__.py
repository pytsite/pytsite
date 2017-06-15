"""Pytsite Form Package.
"""
# Public API
from . import _error as error, _cache as cache
from ._form import Form

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


def _init():
    from pytsite import assetman, tpl, lang, router, http_api, cron, stats
    from . import _controllers, _http_api_controllers

    lang.register_package(__name__)
    tpl.register_package(__name__)

    assetman.register_package(__name__)
    assetman.t_less(__name__ + '@**/*.less')
    assetman.t_js(__name__ + '@**/*.js')
    assetman.js_module('pytsite-form', __name__ + '@js/pytsite-form')

    router.handle(_controllers.Submit(), '/form/submit/<uid>', 'pytsite.form@submit', methods='POST')

    http_api.handle('POST', 'form/widgets/<uid>', _http_api_controllers.GetWidgets(), 'pytsite.form@post_get_widgets')
    http_api.handle('POST', 'form/validate/<uid>', _http_api_controllers.PostValidate(), 'pytsite.form@post_validate')

    # Cron tasks
    cron.every_min(cache.cleanup)

    # Stats update
    stats.on_update(lambda: 'Forms cache size: {}'.format(cache.get_size()))


_init()
