"""PytSite Currency Package.
"""
# Public API
from ._api import get_all, get_main
from . import _widget as widget, _error as error

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


def __init():
    """Init wrapper.
    """
    from pytsite import reg, tpl, lang, settings
    from . import _api, _form

    # Language package
    lang.register_package(__name__)

    # Loading currencies from registry config
    for code in reg.get('currency.currencies', ('USD',)):
        _api.define(code)

    # Settings form
    settings.define('currency', _form.Settings, __name__ + '@currency', 'fa fa-dollar')

    # Tpl globals
    tpl.register_global('currency', _api)


# Package initialization
__init()
