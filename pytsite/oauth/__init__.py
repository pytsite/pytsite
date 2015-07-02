"""PytSite oAuth.
"""
__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

def __init():
    import sys
    from pytsite import admin, odm_ui
    from pytsite.core import odm, tpl, lang, router
    from ._model import Account

    lang.register_package(__name__)
    tpl.register_global('oauth', sys.modules[__name__])
    odm.register_model('oauth_account', Account )

    href = router.endpoint_url('pytsite.odm_ui.eps.browse', {'model': 'oauth_account'})
    admin.sidebar.add_menu('misc', 'oauth_accounts', 'pytsite.oauth@oauth', href, 'fa fa-user',
                           permissions=(
                               'pytsite.odm_ui.browse.oauth_account',
                               'pytsite.odm_ui.browse_own.oauth_account'
                           ))

__init()


# Public API
from . import _widget as widget
