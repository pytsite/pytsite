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

    # 'Security' admin sidebar section
    if not admin.sidebar.get_section('auth'):
        admin.sidebar.add_section('auth', 'pytsite.auth@security', 1000,
                                  permissions=('pytsite.odm_perm.view.user', 'pytsite.odm_perm.view.role'))

    admin_href = router.ep_path('pytsite.odm_ui@browse', {'model': 'auth_log'})
    admin.sidebar.add_menu('auth', 'auth_log', 'pytsite.auth_log@log', admin_href, 'fa fa-history',
                           weight=30, permissions='pytsite.odm_perm.delete.auth_log')

__init()
