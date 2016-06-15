"""Event Handlers.
"""
from datetime import datetime as _datetime
from pytsite import lang as _lang, console as _console, router as _router, validation as _validation, util as _util, \
    hreflang as _hreflang, reg as _reg
from . import _api

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


def pytsite_setup():
    """'pytsite.setup' Event Handler
    """
    # Creating administrator
    email = input(_lang.t('pytsite.auth@enter_admin_email') + ': ')
    try:
        _validation.rule.NonEmpty(email, 'pytsite.auth@email_cannot_be_empty').validate()
        _validation.rule.Email(email).validate()
    except _validation.error.RuleError as e:
        raise _console.error.Error(e)

    admin_user = _api.create_user(email)
    admin_user.f_set('first_name', _lang.t('pytsite.auth@administrator'))
    admin_user.f_set('nickname', _util.transform_str_2(admin_user.full_name))
    admin_user.f_add('roles', _api.get_role('admin'))
    admin_user.save()
    _console.print_success(_lang.t('pytsite.auth@user_has_been_created', {'login': admin_user.f_get('login')}))


def pytsite_router_dispatch():
    """pytsite.router.dispatch Event Handler.
    """
    # Determine current user based on session's data
    if 'pytsite.auth.login' in _router.session():
        user = _api.get_user(_router.session()['pytsite.auth.login'])

    # Determine current user based on request's argument
    elif 'access_token' in _router.request().inp:
        user = _api.get_user(access_token=_router.request().inp['access_token'])

    else:
        user = _api.get_anonymous_user()

    # Set current user
    _api.set_current_user(user)

    if not user.is_anonymous and not user.is_system:
        if user.status == 'active':
            # Update user's activity timestamp
            _router.set_no_cache(True)
            user.f_set('last_activity', _datetime.now()).save(True, False)
        else:
            # Sign out inactive user
            _api.sign_out(user)

    # Alternate languages for sign in page
    if len(_lang.langs()) > 1:
        base_path = _reg.get('auth.base_path', '/auth/login')
        if base_path == _router.current_path(True):
            for lng in _lang.langs(False):
                _hreflang.add(lng, _router.url(base_path, lang=lng))


def pytsite_update(version: str):
    """'pytsite.update' event handler.
    """
    if version == '0.13.0':
        for user in _api.find_users(False).get():
            if not user.nickname:
                if not user.full_name:
                    user.f_set('first_name', _util.random_str())
                user.f_set('nickname', _util.transform_str_2(user.full_name)).save()
                _console.print_info('User updated: {}'.format(user.login))
