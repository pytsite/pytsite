"""Auth UI.
"""
# Public API
from . import _widget as widget, _model as model

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


def __init():
    from pytsite import admin, odm, tpl, lang, router, assetman, robots, reg, util, ajax
    from . import _model

    # Resources
    lang.register_package(__name__)
    tpl.register_package(__name__)

    # Routes
    base_path = reg.get('auth_ui.base_path', '/auth_ui')
    router.add_rule(base_path + '/profile/<string:nickname>', 'pytsite.auth_ui.ep.profile_view')
    router.add_rule(base_path + '/profile/<string:nickname>/edit', 'pytsite.auth_ui.ep.profile_edit',
                    filters='pytsite.auth.ep.filter_authorize')
    router.add_rule(base_path + '/profile/<string:nickname>/edit/submit', 'pytsite.auth_ui.ep.profile_edit_submit',
                    methods='POST')

    # Replace 'user' and 'role' models with UI-compatible
    user_cls = util.get_class(reg.get('auth_ui.model.user', 'pytsite.auth_ui._model.UserUI'))
    odm.register_model('user', user_cls, True)
    role_cls = util.get_class(reg.get('auth_ui.model.role', 'pytsite.auth_ui._model.RoleUI'))
    odm.register_model('role', role_cls, True)

    # 'Security' admin sidebar section
    admin.sidebar.add_section('auth', 'pytsite.auth_ui@security', 1000,
                              permissions=('pytsite.odm_ui.browse.user', 'pytsite.odm_ui.browse.role'))

    # 'Users' admin sidebar menu
    url = router.ep_url('pytsite.odm_ui.ep.browse', {'model': 'user'})
    admin.sidebar.add_menu('auth', 'users', 'pytsite.auth_ui@users', url, 'fa fa-user', weight=10,
                           permissions=('pytsite.odm_ui.browse.user',))

    # 'Roles' admin sidebar menu
    url = router.ep_url('pytsite.odm_ui.ep.browse', {'model': 'role'})
    admin.sidebar.add_menu('auth', 'roles', 'pytsite.auth_ui@roles', url, 'fa fa-users', weight=20,
                           permissions=('pytsite.odm_ui.browse.role',))

    # Assets
    assetman.register_package(__name__)

    # robots.txt rules
    robots.disallow(base_path + '/')

    # AJAX API endpoints
    ajax.register_ep('pytsite.auth_ui.ajax.follow')

__init()
