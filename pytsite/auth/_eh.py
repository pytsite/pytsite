"""Event Handlers.
"""
from datetime import datetime as _datetime
from pytsite import lang as _lang, console as _console, router as _router, validation as _validation, util as _util, \
    hreflang as _hreflang, reg as _reg
from . import _api, _error

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


def pytsite_setup():
    """'pytsite.setup' Event Handler
    """
    # Searching for an administrator
    if len(list(_api.get_users(roles=(_api.get_role('admin'),)))):
        return

    # Creating administrator
    email = input(_lang.t('pytsite.auth@enter_admin_email') + ': ')
    try:
        _validation.rule.NonEmpty(email, 'pytsite.auth@email_cannot_be_empty').validate()
        _validation.rule.Email(email).validate()
    except _validation.error.RuleError as e:
        raise _console.error.Error(e)

    admin_user = _api.create_user(email)
    admin_user.first_name = _lang.t('pytsite.auth@administrator')
    admin_user.nickname = _util.transform_str_2(admin_user.full_name)
    admin_user.roles = [_api.get_role('admin')]
    admin_user.storage_save()
    _console.print_success(_lang.t('pytsite.auth@user_has_been_created', {'login': admin_user.login}))


def pytsite_router_dispatch():
    """pytsite.router.dispatch Event Handler.
    """
    user = _api.get_anonymous_user()

    # Determine current user based on session's data
    if 'pytsite.auth.login' in _router.session():
        try:
            user = _api.get_user(_router.session()['pytsite.auth.login'])
        except _error.UserNotExist:
            del _router.session()['pytsite.auth.login']
            user = _api.get_anonymous_user()

    # Determine current user based on request's argument
    elif 'access_token' in _router.request().inp:
        try:
            user = _api.get_user(access_token=_router.request().inp['access_token'])
        except _error.UserNotExist:
            user = _api.get_anonymous_user()

    # Set current user
    _api.switch_user(user)

    if not user.is_anonymous:
        if user.status == 'active':
            # Update user's activity timestamp
            _router.set_no_cache(True)
            user.last_activity = _datetime.now()
            user.storage_save()
        else:
            # Sign out inactive user
            _api.sign_out(user)

    # Alternate languages for sign in page
    if len(_lang.langs()) > 1:
        base_path = _reg.get('auth.base_path', '/auth/login')
        if base_path == _router.current_path(True):
            for lng in _lang.langs(False):
                _hreflang.add(lng, _router.url(base_path, lang=lng))
