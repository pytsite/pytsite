"""Auth Log Package Init.
"""

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


def __init():
    from pytsite import events, odm, admin, lang, router
    from . import _eh, _model

    lang.register_package(__name__)

    odm.register_model('auth_log', _model.AuthLog)
    events.listen('pytsite.auth.sign_in', _eh.auth_sign_in)
    events.listen('pytsite.auth.sign_out', _eh.auth_sign_out)
    events.listen('pytsite.auth.sign_in_error', _eh.auth_sign_in_error)

    admin_href = router.ep_url('pytsite.odm_ui.ep.browse', {'model': 'auth_log'})
    admin.sidebar.add_menu('auth', 'auth_log', 'pytsite.auth_log@log', admin_href, 'fa fa-history',
                           weight=30, permissions='pytsite.odm_ui.browse.auth_log')

__init()
