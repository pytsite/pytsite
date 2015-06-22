"""Currency Plugin Package
"""
__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


def __init():
    """Init wrapper.
    """
    from pytsite.core import lang, reg, tpl
    from pytsite import settings
    from . import _functions, _form

    # Language package
    lang.register_package(__name__)

    # Loading currencies from registry config
    for code in reg.get('currency.currencies'):
        _functions.define(code)

    # Setting
    settings.define('currency', _form.Settings, __name__ + '@currency', 'fa fa-dollar')

    # Tpl globals
    tpl.register_global('currency', _functions)


# Package initialization
__init()

# Public API
from ._functions import get_currencies
from . import _widget as widget, _odm_field as odm_field
