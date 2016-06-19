""" PytSite Auth Module Init.
"""
# Public API
from . import _error as error, _model as model, _driver as driver, _widget as widget
from ._api import get_current_user, get_user_statuses, get_user, create_user, get_role, get_sign_in_form, \
    register_auth_driver, user_nickname_rule, sign_in, get_auth_driver, create_role, get_sign_in_url, get_sign_out_url,\
    verify_password, hash_password, sign_out, get_access_token_info, switch_user, get_anonymous_user, \
    get_system_user, get_users, get_storage_driver, register_storage_driver

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


def __init():
    """Init wrapper.
    """
    from pytsite import reg, assetman, events, tpl, lang, router, robots, console, permission, util
    from ._console_command import Passwd as AuthConsoleCommand
    from . import _eh

    # Resources
    tpl.register_package(__name__)
    lang.register_package(__name__)
    assetman.register_package(__name__)
    assetman.add('pytsite.auth@js/auth.js', permanent=True)

    # Routes
    base_path = reg.get('auth.routes.base_path', '/auth')
    router.add_rule(base_path + '/sign-in/<driver>', 'pytsite.auth@sign_in')
    router.add_rule(base_path + '/sign-in/<driver>/post', 'pytsite.auth@sign_in_submit', methods='POST')
    router.add_rule(base_path + '/sign-out/<driver>', 'pytsite.auth@sign_out')
    router.add_rule(base_path + '/profile/<nickname>', 'pytsite.auth@profile_view')
    router.add_rule(base_path + '/profile/<nickname>/edit', 'pytsite.auth@profile_edit',
                    filters='pytsite.auth@filter_authorize')
    router.add_rule(base_path + '/profile/<nickname>/edit/submit', 'pytsite.auth@profile_edit_submit',
                    methods='POST')

    # Template engine globals
    tpl.register_global('auth_current_user', get_current_user)
    tpl.register_global('auth_sign_in_url', get_sign_in_url)
    tpl.register_global('auth_sign_out_url', get_sign_out_url)

    # Event handlers
    events.listen('pytsite.setup', _eh.pytsite_setup)
    events.listen('pytsite.router.dispatch', _eh.pytsite_router_dispatch)

    # Permissions
    permission.define_permission_group('auth', 'pytsite.auth@auth_permission_group_description')
    permission.define_permission('admin', 'pytsite.auth@admin_permission_description', 'auth')

    # robots.txt rules
    robots.disallow(base_path + '/')

    # Console commands
    console.register_command(AuthConsoleCommand())

    # Load storage driver
    driver_class = util.get_class(reg.get('auth.storage_driver', 'pytsite.auth_storage_odm.Driver'))
    register_storage_driver(driver_class())

    # Set system user as current
    switch_user(get_system_user())

    # Required roles
    for r_name in ('anonymous', 'user', 'admin'):
        try:
            _api.get_role(r_name)
        except error.RoleNotExist:
            _api.create_role(r_name, 'pytsite.auth@{}_role_description'.format(r_name)).save()

    # robots.txt rules
    robots.disallow(base_path + '/')

__init()
