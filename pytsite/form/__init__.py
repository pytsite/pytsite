"""Pytsite Form Package.
"""
# Public API
from . import _error as error
from ._form import Form


__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


def _init():
    from pytsite import assetman, tpl, lang, ajax

    lang.register_package(__name__)
    assetman.register_package(__name__)
    tpl.register_package(__name__)

    # AJAX endpoints
    ajax.register_ep('pytsite.form.ajax.get_widgets')
    ajax.register_ep('pytsite.form.ajax.validate')

_init()
