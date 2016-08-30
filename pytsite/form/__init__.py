"""Pytsite Form Package.
"""
# Public API
from . import _error as error
from ._form import Form


__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


def _init():
    from pytsite import assetman, tpl, lang, http_api

    lang.register_package(__name__)
    assetman.register_package(__name__)
    tpl.register_package(__name__)
    http_api.register_package('form', 'pytsite.form.http_api')


_init()
