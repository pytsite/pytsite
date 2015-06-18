"""Currency Plugin Package
"""
__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


def __init():
    """Init wrapper.
    """
    from pytsite.core import lang, reg
    from pytsite import settings
    from . import _functions, _form

    # Language package
    lang.register_package(__name__)

    # Loading currencies from registry config
    for code in reg.get('currency.currencies'):
        _functions.define(code)

    # Setting
    settings.define('currency', _form.Settings, __name__ + '@currency', 'fa fa-dollar')


# Package initialization
__init()

# Public API
from ._functions import get_currencies