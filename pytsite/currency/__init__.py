"""PytSite Currency Package.
"""
# Public API
from . import _model as model
from ._api import define, get_all, get_main, set_main, get_rate, exchange, fmt, get_title, get_symbol
from . import _widget as widget, _error as error

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


def __init():
    """Init wrapper.
    """
    from pytsite import reg, tpl, lang, admin, router, odm, events
    from . import _api, _model, _eh

    # Language package
    lang.register_package(__name__)

    # Loading currencies from registry config
    for code in reg.get('currency.currencies', ('USD',)):
        _api.define(code)

    # Tpl globals
    tpl.register_global('currency_fmt', _api.fmt)

    # ODM models
    odm.register_model('currency_rate', model.Rate)

    # Admin menu
    admin.sidebar.add_section('currency', 'pytsite.currency@currency', 260)
    admin.sidebar.add_menu('currency', 'rates', 'pytsite.currency@rates',
                           router.ep_url('pytsite.odm_ui.ep.browse', {'model': 'currency_rate'}),
                           'fa fa-usd', weight=10, permissions='pytsite.odm_ui.browse.currency_rate')

    # Event handlers
    events.listen('pytsite.odm.model.user.setup_fields', _eh.odm_model_user_setup)
    events.listen('pytsite.odm_ui.user.m_form_setup_widgets', _eh.odm_ui_user_m_form_setup_widgets)


# Package initialization
__init()
