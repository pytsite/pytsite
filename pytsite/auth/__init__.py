""" PytSite Auth Module Init.
"""
# Public API
from . import _error as error, _model as model
from ._api import get_current_user, get_user_statuses, get_user, create_user, get_role, get_login_form, find_users, \
    register_driver, get_default_driver, user_nickname_rule

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


def __init():
    """Init wrapper.
    """
    from pytsite import reg, assetman, odm, events, tpl, lang, router, robots, console, ajax, permission
    from ._console_command import Passwd as AuthConsoleCommand
    from . import _eh

    # Resources
    tpl.register_package(__name__)
    lang.register_package(__name__)
    assetman.register_package(__name__)
    assetman.add('pytsite.auth@js/auth.js', permanent=True)

    # ODM models
    from . import _model
    odm.register_model('user', _model.User)
    odm.register_model('role', _model.Role)

    # Auth drivers
    from .driver import ulogin, password
    register_driver(ulogin.Driver())
    register_driver(password.Driver())

    # Routes
    base_path = reg.get('auth.base_path', '/auth')
    router.add_rule(base_path + '/login/<driver>', 'pytsite.auth.ep.login')
    router.add_rule(base_path + '/login/<driver>/post', 'pytsite.auth.ep.login_submit', methods='POST')
    router.add_rule(base_path + '/logout', 'pytsite.auth.ep.logout')

    # AJAX endpoints
    ajax.register_ep('pytsite.auth.ajax.get_login_form')
    ajax.register_ep('pytsite.auth.ajax.is_anonymous')

    # Template engine globals
    tpl.register_global('auth_current_user', _api.get_current_user)
    tpl.register_global('auth_login_url', _api.get_login_url)
    tpl.register_global('auth_logout_url', _api.get_logout_url)

    # Event handlers
    events.listen('pytsite.setup', _eh.pytsite_setup)
    events.listen('pytsite.router.dispatch', _eh.pytsite_router_dispatch)
    events.listen('pytsite.update', _eh.pytsite_update)

    # Permissions
    permission.define_permission_group('auth', 'pytsite.auth@auth_permission_group_description')
    permission.define_permission('admin', 'pytsite.auth@admin_permission_description', 'auth')

    # robots.txt rules
    robots.disallow(base_path + '/')

    # Console commands
    console.register_command(AuthConsoleCommand())

__init()
