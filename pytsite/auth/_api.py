"""Auth Manager.
"""
from collections import OrderedDict
from datetime import datetime as _datetime
from pytsite import reg as _reg, http as _http, odm as _odm, form as _form, lang as _lang, router as _router, \
    events as _events, validation as _validation, geo_ip as _geo_ip
from .driver.abstract import AbstractDriver as _AbstractDriver
from . import _error, _model

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

_drivers = OrderedDict()
""":type: dict[_AbstractDriver]"""

__permission_groups = []
__permissions = []
__anonymous_user = None

user_login_rule = _validation.rule.Email()
user_nickname_rule = _validation.rule.Regex(msg_id='pytsite.auth@nickname_str_rules',
                                            pattern='^[A-Za-z0-9][A-Za-z0-9\.\-_]{0,31}$')


def password_hash(secret: str) -> str:
    """Hash a password.
    """
    from werkzeug.security import generate_password_hash
    return generate_password_hash(secret)


def password_verify(clear_text: str, hashed: str) -> bool:
    """Verify hashed password.
    """
    from werkzeug.security import check_password_hash
    return check_password_hash(hashed, clear_text)


def register_driver(driver: _AbstractDriver):
    """Change current driver.
    """
    if not isinstance(driver, _AbstractDriver):
        raise TypeError('Instance of AbstractDriver expected.')

    name = driver.get_name()
    if name in _drivers:
        raise ValueError("Driver '{}' is already registered.".format(name))

    _drivers[name] = driver


def get_driver(name: str = None) -> _AbstractDriver:
    """Get current driver.
    """
    if not name:
        if _drivers:
            name = next(iter(_drivers.values())).get_name()
        else:
            raise Exception('No driver registered.')

    if name not in _drivers:
        raise _error.DriverNotRegistered("Driver '{}' is not registered.".format(name))

    return _drivers[name]


def get_default_driver() -> _AbstractDriver:
    """Get default driver.
    """
    return get_driver(_reg.get('auth.default_driver'))


def get_login_form(driver_name: str = None, uid: str = None, **kwargs) -> _form.Form:
    """Get a login form.
    """
    driver = get_driver(driver_name)

    kwargs['css'] = kwargs.get('css', '') + ' pytsite-auth-login driver-' + driver.name

    if not uid:
        uid = 'pytsite-auth-login'

    if not kwargs.get('title'):
        kwargs['title'] = _lang.t('pytsite.auth@authorization')

    form = driver.get_login_form(uid, **kwargs)
    form.action = _router.ep_url('pytsite.auth.ep.login_submit', {'driver': driver.name})

    return form


def post_login_form(driver_name: str, inp: dict) -> _http.response.Redirect:
    """Post a login form.
    """
    for i in ('__form_steps', '__form_step'):
        if i in inp:
            del inp[i]

    return get_driver(driver_name).post_login_form(inp)


def create_user(login: str, password: str = None) -> _model.User:
    """Create new user.
    """
    if login != _model.ANONYMOUS_USER_LOGIN:
        if get_user(login):
            raise RuntimeError("User with login '{}' already exists.".format(login))

        user_login_rule.value = login
        user_login_rule.validate()

    user = _odm.dispense('user')  # type: _model.User
    user.f_set('login', login).f_set('email', login).f_set('password', password)

    if login != _model.ANONYMOUS_USER_LOGIN:
        # Automatic roles for new users
        for role_name in _reg.get('auth.signup.roles', ['user']):
            role = get_role(role_name)
            if role:
                user.f_add('roles', role)

        # GeoIP data
        if _router.request():
            user.f_set('geo_ip', _geo_ip.resolve(_router.request().remote_addr))

        user.save()
        _events.fire('pytsite.auth.user.create', user=user)

    return user


def get_user(login: str = None, uid: str = None, nickname: str = None) -> _model.User:
    """Get user by login or by uid.
    """
    # Don't cache finder results due to frequent user updates in database
    f = _odm.find('user').cache(0)
    if login:
        if login == _model.ANONYMOUS_USER_LOGIN:
            return None
        return f.where('login', '=', login).first()
    elif uid:
        return f.where('_id', '=', uid).first()
    elif nickname:
        return f.where('nickname', '=', nickname).first()


def create_role(name: str, description: str = ''):
    """Create new role.
    """
    if get_role(name=name):
        raise Exception("Role with name '{}' already exists.".format(name))

    role = _odm.dispense('role')
    return role.f_set('name', name).f_set('description', description)


def get_role(name: str = None, uid=None) -> _model.Role:
    """Get role by name or by UID.
    """
    if name:
        return _odm.find('role').where('name', '=', name).first()
    if uid:
        return _odm.find('role').where('_id', '=', uid).first()


def authorize(user: _model.User, count_login: bool = True, issue_event: bool = True,
              update_geo_ip: bool = True) -> _model.User:
    """Authorize user.
    """
    if not user:
        raise _error.LoginError('pytsite.auth@authorization_error')

    # Checking user status
    if user.f_get('status') != 'active':
        logout_current_user(issue_event)
        raise _error.LoginError('pytsite.auth@authorization_error')

    # Update login counter
    if count_login:
        user.f_inc('login_count').f_set('last_login', _datetime.now()).save()

    # Update IP address and geo data
    if update_geo_ip and _router.request():
        user.f_set('last_ip', _router.request().remote_addr)
        if not user.country and user.geo_ip.country:
            user.f_set('country', user.geo_ip.country)
        if not user.city and user.geo_ip.city:
            user.f_set('city', user.geo_ip.city)

        user.save()

    # Login event
    if issue_event:
        _events.fire('pytsite.auth.login', user=user)

    _router.session()['pytsite.auth.login'] = user.login

    return user


def get_anonymous_user() -> _model.User:
    """Get anonymous user.
    """
    global __anonymous_user
    if not __anonymous_user:
        __anonymous_user = create_user(_model.ANONYMOUS_USER_LOGIN)

    return __anonymous_user


def get_current_user() -> _model.User:
    """Get currently authorized user.
    """
    if not _router.session():
        return get_anonymous_user()

    login = _router.session().get('pytsite.auth.login')
    if not login:
        return get_anonymous_user()

    try:
        user = get_user(login=login)
        if not user:
            return get_anonymous_user()

        return authorize(user, False, False, False)

    except _error.LoginError:
        return get_anonymous_user()


def logout_current_user(issue_event=True):
    """Log out current user.
    """
    user = get_current_user()
    if not user.is_anonymous:
        if issue_event:
            _events.fire('pytsite.auth.logout', user=user)
        del _router.session()['pytsite.auth.login']


def get_user_statuses() -> tuple:
    """Get available user statuses.
    """
    return (
        ('active', _lang.t('pytsite.auth@status_active')),
        ('waiting', _lang.t('pytsite.auth@status_waiting')),
        ('disabled', _lang.t('pytsite.auth@status_disabled')),
    )


def get_login_url(driver: str = 'ulogin') -> str:
    """Get login URL.
    """
    return _router.ep_url('pytsite.auth.ep.login', {'driver': driver})


def get_logout_url() -> str:
    """Get logout URL.
    """
    return _router.ep_url('pytsite.auth.ep.logout', {'__redirect': _router.current_url()})


def find_users(active_only: bool = True) -> _odm.Finder:
    """Get users finder.
    """
    f = _odm.find('user').sort([('login_count', _odm.I_DESC)])
    if active_only:
        f.where('status', '=', 'active')

    return f
