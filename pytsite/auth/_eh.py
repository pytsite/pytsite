"""PytSite Auth Event Handlers
"""
from datetime import datetime as _datetime
from pytsite import lang as _lang, console as _console, router as _router, validation as _validation, util as _util, \
    hreflang as _hreflang, reg as _reg, http as _http
from . import _api, _error

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


def setup():
    """'pytsite.setup' Event Handler
    """
    # Searching for an administrator
    if _api.count_users({'roles': [_api.get_role('admin')]}):
        return

    # Creating administrator
    email = input(_lang.t('pytsite.auth@enter_admin_email') + ': ')
    try:
        _validation.rule.NonEmpty(email, 'pytsite.auth@email_cannot_be_empty').validate()
        _validation.rule.Email(email).validate()
    except _validation.error.RuleError as e:
        raise _console.error.Error(e)

    _api.switch_user_to_system()
    admin_user = _api.create_user(email)
    admin_user.first_name = _lang.t('pytsite.auth@administrator')
    admin_user.nickname = _util.transform_str_2(admin_user.full_name)
    admin_user.roles = [_api.get_role('admin')]
    admin_user.save()
    _api.restore_user()
    _console.print_success(_lang.t('pytsite.auth@user_has_been_created', {'login': admin_user.login}))


def router_dispatch():
    """pytsite.router.dispatch Event Handler.
    """
    user = _api.get_anonymous_user()

    # Determine current user based on session's data
    if 'pytsite.auth.login' in _router.session():
        try:
            user = _api.get_user(_router.session()['pytsite.auth.login'])
        except _error.UserNotExist:
            # User has been deleted, so delete session information about it
            del _router.session()['pytsite.auth.login']

    # Set current user
    _api.switch_user(user)

    if not user.is_anonymous:
        if user.status == 'active':
            # Disable page caching for signed in users
            _router.set_no_cache(True)

            # Update user's activity timestamp
            user.last_activity = _datetime.now()
            user.save()
        else:
            # Sign out inactive user
            _api.sign_out(user)

    # Alternate languages for sign in page
    if len(_lang.langs()) > 1:
        base_path = _reg.get('auth.base_path', '/auth/login')
        if base_path == _router.current_path(True):
            for lng in _lang.langs(False):
                _hreflang.add(lng, _router.url(base_path, lang=lng))


def router_response(response: _http.response.Response):
    if 'PYTSITE_SESSION' in _router.request().cookies and _api.get_current_user().is_anonymous:
        response.delete_cookie('PYTSITE_SESSION')


def http_api_pre_request():
    # Authorize user by access token
    access_token = _router.request().headers.get('PytSite-Auth')

    if not access_token:
        return

    try:
        _api.switch_user(_api.get_user(access_token=access_token))
        _api.prolong_access_token(access_token)

    except (_error.InvalidAccessToken, _error.UserNotExist, _error.AuthenticationError) as e:
        raise _http.error.Forbidden(response=_http.response.JSON({'error': str(e)}))
