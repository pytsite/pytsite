"""Pytsite Form Package.
"""
# Public API
from . import _error as error, _cache as cache
from ._form import Form


__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


def _init():
    from pytsite import assetman, tpl, lang, router, http_api, events
    from . import _http_api

    lang.register_package(__name__)
    assetman.register_package(__name__)
    tpl.register_package(__name__)

    router.add_rule('/form/submit/<uid>', 'pytsite.form@submit')

    http_api.handle('POST', 'form/widgets/<uid>', _http_api.get_widgets, 'pytsite.form@post_get_widgets')
    http_api.handle('POST', 'form/validate/<uid>', _http_api.post_validate, 'pytsite.form@post_validate')

    events.listen('pytsite.cron.1min', cache.cleanup)


_init()
