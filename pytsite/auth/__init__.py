""" PytSite Authentication and Authorization.
"""
# Public API
from . import _error as error, _model as model, _driver as driver, _widget as widget
from ._api import get_current_user, get_user_statuses, get_user, create_user, get_role, get_sign_in_form, \
    register_auth_driver, user_nickname_rule, sign_in, get_auth_driver, create_role, get_sign_in_url, \
    get_sign_out_url, verify_password, hash_password, sign_out, get_access_token_info, switch_user, \
    get_anonymous_user, get_system_user, get_users, get_storage_driver, count_users, count_roles, \
    get_first_admin_user, get_roles, get_user_modify_form, base_path, switch_user_to_system, switch_user_to_anonymous, \
    restore_user, generate_access_token, prolong_access_token, register_storage_driver

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


def __init():
    """Init wrapper.
    """
    from pytsite import assetman, tpl, lang, router, robots, console, http_api, permissions, setup
    from ._console_command import Passwd as AuthConsoleCommand
    from . import _eh, _controllers, _http_api_controllers

    # Resources
    tpl.register_package(__name__)
    lang.register_package(__name__)
    assetman.register_package(__name__)
    assetman.t_js('pytsite.auth@**/*.js')
    assetman.t_less('pytsite.auth@**/*.less')
    assetman.js_module('pytsite-auth', __name__ + '@js/pytsite-auth')
    assetman.js_module('pytsite-auth-widget-follow', __name__ + '@js/pytsite-auth-widget-follow')
    assetman.js_module('pytsite-auth-widget-profile', __name__ + '@js/pytsite-auth-widget-profile')

    # Module permission group
    permissions.define_group('security', 'pytsite.auth@security')

    # Access token HTTP API
    http_api.handle('POST', 'auth/access-token/<driver>', _http_api_controllers.PostAccessToken(),
                    'pytsite.auth@post_access_token')
    http_api.handle('GET', 'auth/access-token/<token>', _http_api_controllers.GetAccessToken(),
                    'pytsite.auth@get_access_token')
    http_api.handle('DELETE', 'auth/access-token/<token>', _http_api_controllers.DeleteAccessToken(),
                    'pytsite.auth@delete_access_token')

    # User HTTP API
    http_api.handle('GET', 'auth/is_anonymous', _http_api_controllers.IsAnonymous(), 'pytsite.auth@is_anonymous')
    http_api.handle('GET', 'auth/user/<uid>', _http_api_controllers.GetUser(), 'pytsite.auth@get_user')
    http_api.handle('PATCH', 'auth/user/<uid>', _http_api_controllers.PatchUser(), 'pytsite.auth@patch_user')

    # Following HTTP API
    http_api.handle('POST', 'auth/follow/<uid>', _http_api_controllers.PostFollow(), 'pytsite.auth@post_follow')
    http_api.handle('DELETE', 'auth/follow/<uid>', _http_api_controllers.DeleteFollow(), 'pytsite.auth@delete_follow')

    # Routes
    bp = base_path()
    router.handle(_controllers.FilterAuthorize(), name='pytsite.auth@authorize')
    router.handle(_controllers.SignIn(), bp + '/sign-in/<driver>', 'pytsite.auth@sign_in')
    router.handle(_controllers.SignInSubmit(), bp + '/sign-in/<driver>/post', 'pytsite.auth@sign_in_submit',
                  methods='POST')
    router.handle(_controllers.SignOut(), bp + '/sign-out', 'pytsite.auth@sign_out')
    router.handle(_controllers.ProfileView(), bp + '/profile/<nickname>', 'pytsite.auth@profile_view')
    router.handle(_controllers.ProfileEdit(), bp + '/profile/<nickname>/edit', 'pytsite.auth@profile_edit',
                  filters='pytsite.auth@authorize')

    # Template engine globals
    tpl.register_global('auth_current_user', get_current_user)
    tpl.register_global('auth_sign_in_url', get_sign_in_url)
    tpl.register_global('auth_sign_out_url', get_sign_out_url)

    # Event handlers
    setup.on_setup(_eh.setup)
    router.on_dispatch(_eh.router_dispatch, -999, '*')
    router.on_xhr_dispatch(_eh.router_dispatch, -999, '*')
    router.on_response(_eh.router_response, -999, '*')
    router.on_xhr_response(_eh.router_response, -999, '*')
    http_api.on_pre_request(_eh.http_api_pre_request)

    # Console commands
    console.register_command(AuthConsoleCommand())

    # robots.txt rules
    robots.disallow(bp + '/')


__init()
