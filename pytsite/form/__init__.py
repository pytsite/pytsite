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

    lang.register_package(__name__)
    assetman.register_package(__name__)
    tpl.register_package(__name__)

    router.add_rule('/form/submit/<uid>', 'pytsite.form@submit')
    http_api.register_handler('form', 'pytsite.form.http_api')

    events.listen('pytsite.cron.1min', cache.cleanup)


_init()
