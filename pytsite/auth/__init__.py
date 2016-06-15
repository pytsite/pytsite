""" PytSite Auth Module Init.
"""
# Public API
from . import _error as error, _model as model, _driver as driver
from ._api import get_current_user, get_user_statuses, get_user, create_user, get_role, get_sign_in_form, find_users, \
    register_driver, user_nickname_rule, sign_in, get_driver, create_role, get_sign_in_url, get_sign_out_url, \
    verify_password, hash_password, sign_out, get_access_token_info, sanitize_nickname, set_current_user, \
    get_anonymous_user, get_system_user

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


def __init():
    """Init wrapper.
    """
    from pytsite import reg, assetman, odm, events, tpl, lang, router, robots, console, permission
    from ._console_command import Passwd as AuthConsoleCommand
    from . import _eh

    # Resources
    tpl.register_package(__name__)
    lang.register_package(__name__)
    assetman.register_package(__name__)
    assetman.add('pytsite.auth@js/auth.js', permanent=True)

    # ODM models
    odm.register_model('user', model.User)
    odm.register_model('role', model.Role)

    # Routes
    base_path = reg.get('auth.base_path', '/auth')
    router.add_rule(base_path + '/sign-in/<driver>', 'pytsite.auth@sign_in')
    router.add_rule(base_path + '/sign-in/<driver>/post', 'pytsite.auth@sign_in_submit', methods='POST')
    router.add_rule(base_path + '/sign-out/<driver>', 'pytsite.auth@sign_out')

    # Template engine globals
    tpl.register_global('auth_current_user', _api.get_current_user)
    tpl.register_global('auth_sign_in_url', _api.get_sign_in_url)
    tpl.register_global('auth_sign_out_url', _api.get_sign_out_url)

    # Event handlers
    events.listen('pytsite.setup', _eh.pytsite_setup)
    events.listen('pytsite.router.dispatch', _eh.pytsite_router_dispatch)
    events.listen('pytsite.update', _eh.pytsite_update)

    # Required roles
    for r_name in ('anonymous', 'user', 'admin'):
        if not _api.get_role(r_name):
            _api.create_role(r_name, 'pytsite.auth@{}_role_description'.format(r_name)).save()

    # Permissions
    permission.define_permission_group('auth', 'pytsite.auth@auth_permission_group_description')
    permission.define_permission('admin', 'pytsite.auth@admin_permission_description', 'auth')

    # robots.txt rules
    robots.disallow(base_path + '/')

    # Console commands
    console.register_command(AuthConsoleCommand())

__init()
