"""Auth UI.
"""
# Public API
from . import _widget as widget

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

# Requirements
__import__('pytsite.odm_ui')
__import__('pytsite.image')


def __init():
    from sys import modules
    from pytsite import admin
    from pytsite import odm
    from pytsite import tpl
    from pytsite import lang
    from pytsite import router
    from . import _model

    lang.register_package(__name__)
    tpl.register_package(__name__)
    tpl.register_global('auth_ui', modules[__name__])

    # Routes
    router.add_rule('/auth/profile/<string:uid>', __name__ + '.eps.profile_view')
    router.add_rule('/auth/profile/<string:uid>/edit', __name__ + '.eps.profile_edit')
    router.add_rule('/auth/profile/<string:uid>/edit/submit', __name__ + '.eps.profile_edit_submit', methods='POST')

    # Replace 'user' model with UI-compatible
    odm.register_model('user', _model.UserUI, True)
    odm.register_model('role', _model.RoleUI, True)

    # 'Security' admin sidebar section
    admin.sidebar.add_section('auth', 'pytsite.auth_ui@security', 1000,
                              permissions=('pytsite.odm_ui.browse.user', 'pytsite.odm_ui.browse.role'))

    # 'Users' admin sidebar menu
    url = router.endpoint_url('pytsite.odm_ui.eps.browse', {'model': 'user'})
    admin.sidebar.add_menu('auth', 'users', 'pytsite.auth_ui@users', url, 'fa fa-user', weight=10,
                           permissions=('pytsite.odm_ui.browse.user',))

    # 'Roles' admin sidebar menu
    url = router.endpoint_url('pytsite.odm_ui.eps.browse', {'model': 'role'})
    admin.sidebar.add_menu('auth', 'roles', 'pytsite.auth_ui@roles', url, 'fa fa-users', weight=20,
                           permissions=('pytsite.odm_ui.browse.role',))

__init()
