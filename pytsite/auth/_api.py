"""Auth Manager.
"""
from typing import Dict as _Dict, Iterable as _Iterable
from collections import OrderedDict
from datetime import datetime as _datetime, timedelta as _timedelta
from pytsite import reg as _reg, form as _form, lang as _lang, router as _router, cache as _cache, \
    events as _events, validation as _validation, logger as _logger, util as _util, threading as _threading
from . import _error, _model, _driver

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

_authentication_drivers = OrderedDict()  # type: _Dict[str, _driver.Authentication]
_storage_driver = None  # type: _driver.Storage

_permission_groups = []
_permissions = []
_anonymous_user = None
_system_user = None
_access_tokens = _cache.create_pool('pytsite.auth.token_user')  # user.uid: token
_current_user = {}  # user object, per thread
_previous_user = {}  # user object, per thread
_access_token_ttl = _reg.get('auth.access_token_ttl', 86400)  # 24 hours

user_login_rule = _validation.rule.Email()
user_nickname_rule = _validation.rule.Regex(msg_id='pytsite.auth@nickname_str_rules',
                                            pattern='^[A-Za-z0-9][A-Za-z0-9\.\-_]{0,31}$')


def hash_password(secret: str) -> str:
    """Hash a password.
    """
    from werkzeug.security import generate_password_hash
    return generate_password_hash(str(secret))


def verify_password(clear_text: str, hashed: str) -> bool:
    """Verify hashed password.
    """
    from werkzeug.security import check_password_hash
    return check_password_hash(str(hashed), str(clear_text))


def base_path() -> str:
    """Get module routes base path.
    """
    return _reg.get('auth.routes.base_path', '/auth')


def register_auth_driver(driver: _driver.Authentication):
    """Register authentication driver.
    """
    if not isinstance(driver, _driver.Authentication):
        raise TypeError('Instance of pytsite.auth.driver.Authentication expected.')

    name = driver.get_name()
    if name in _authentication_drivers:
        raise RuntimeError("Authentication driver '{}' is already registered.".format(name))

    _authentication_drivers[name] = driver


def get_auth_driver(name: str = None) -> _driver.Authentication:
    """Get driver instance.
    """
    if name is None:
        if _authentication_drivers:
            name = _reg.get('auth.auth_driver', list(_authentication_drivers)[-1])
        else:
            raise _error.NoDriverRegistered('No authentication driver registered')

    if name not in _authentication_drivers:
        raise _error.DriverNotRegistered("Authentication driver '{}' is not registered.".format(name))

    return _authentication_drivers[name]


def register_storage_driver(driver: _driver.Storage):
    """Register storage driver.
    """
    global _storage_driver

    if _storage_driver:
        raise _error.DriverRegistered('Storage driver is already registered')

    if not isinstance(driver, _driver.Storage):
        raise TypeError('Instance of pytsite.auth.driver.Storage expected')

    _storage_driver = driver


def get_storage_driver() -> _driver.Storage:
    """Get driver instance.
    """
    # Load storage driver if it is not loaded yet
    if not _storage_driver:
        raise _error.NoDriverRegistered('No storage driver registered')

    return _storage_driver


def get_sign_in_form(driver_name: str = None, **kwargs) -> _form.Form:
    """Get a login form.
    """
    driver = get_auth_driver(driver_name)

    kwargs['name'] = kwargs.get('name', 'pytsite-auth-sign-in-' + driver.name)
    kwargs['css'] = kwargs.get('css', '') + ' pytsite-auth-sign-in driver-' + driver.name

    form = driver.get_sign_in_form(**kwargs)
    form.action = _router.ep_url('pytsite.auth@sign_in_submit', {'driver': driver.name})

    if not form.title:
        form.title = _lang.t('pytsite.auth@authentication')

    return form


def create_user(login: str, password: str = None) -> _model.AbstractUser:
    """Create new user.
    """
    with _threading.get_shared_r_lock():
        if login not in (_model.ANONYMOUS_USER_LOGIN, _model.SYSTEM_USER_LOGIN):
            # Check user existence
            try:
                get_user(login)
                raise _error.UserExists("User with login '{}' already exists.".format(login))

            except _error.UserNotExist:
                # Check login
                user_login_rule.value = login
                user_login_rule.validate()

        # Create user
        user = get_storage_driver().create_user(login, password)

        # Do some actions with non-anonymous users
        if login not in (_model.ANONYMOUS_USER_LOGIN, _model.SYSTEM_USER_LOGIN):
            # Automatic roles for new users
            roles = []
            for role_name in _reg.get('auth.signup.roles', ['user']):
                try:
                    roles.append(get_role(role_name))
                except _error.RoleNotExist:
                    pass

            user.roles = roles

            user.save()

        return user


def get_user(login: str = None, nickname: str = None, uid: str = None, access_token: str = None) -> _model.AbstractUser:
    """Get user by login, nickname, access token or UID.
    """
    # Convert access token to user UID
    if access_token:
        return get_user(uid=get_access_token_info(access_token)['user_uid'])

    user = get_storage_driver().get_user(login, nickname, uid)

    c_user = get_current_user()
    if user == c_user and user.status != 'active':
        sign_out(user)

    return user


def get_first_admin_user() -> _model.AbstractUser:
    """Get first created user which has 'admin' role.
    """
    users = list(get_users({'roles': [get_role('admin')]}, sort_field='created', limit=1))

    if not users:
        raise _error.NoAdminUser('No admin user created yet.')

    return users[0]


def get_anonymous_user() -> _model.AbstractUser:
    """Get anonymous user.
    """
    global _anonymous_user
    if not _anonymous_user:
        _anonymous_user = create_user(_model.ANONYMOUS_USER_LOGIN)

    return _anonymous_user


def get_system_user() -> _model.AbstractUser:
    """Get system user.
    """
    global _system_user
    if not _system_user:
        _system_user = create_user(_model.SYSTEM_USER_LOGIN)

    return _system_user


def create_role(name: str, description: str = ''):
    """Create new role.
    """
    try:
        get_role(name)
        raise _error.RoleExists("Role with name '{}' already exists.".format(name))

    except _error.RoleNotExist:
        return get_storage_driver().create_role(name, description)


def get_role(name: str = None, uid: str = None) -> _model.AbstractRole:
    """Get role by name or UID.
    """
    # These roles must always exist
    if name in ('anonymous', 'user', 'admin'):
        try:
            get_storage_driver().get_role(name)
        except _error.RoleNotExist:
            switch_user_to_system()
            get_storage_driver().create_role(name, 'pytsite.auth@{}_role_description'.format(name)).save()
            restore_user()

    return get_storage_driver().get_role(name, uid)


def sign_in(auth_driver_name: str, data: dict) -> _model.AbstractUser:
    """Authenticate user.
    """
    with _threading.get_shared_r_lock():
        try:
            # Get user from driver
            user = get_auth_driver(auth_driver_name).sign_in(data)

            if user.status != 'active':
                raise _error.AuthenticationError("User account '{}' is not active.".format(user.login))

            switch_user(user)

        except _error.AuthenticationError as e:
            _logger.warn(str(e))
            raise e

        # Update statistics
        user.sign_in_count += 1
        user.last_sign_in = _datetime.now()
        user.save()

        if _router.request():
            # Set session marker
            _router.session()['pytsite.auth.login'] = user.login

            # Update IP address and geo data
            user.last_ip = _router.request().remote_addr
            if not user.country and user.geo_ip.country:
                user.country = user.geo_ip.country
            if not user.city and user.geo_ip.city:
                user.city = user.geo_ip.city

            user.save()

        # Login event
        _events.fire('pytsite.auth.sign_in', user=user)

        return user


def get_access_token_info(token: str) -> dict:
    """Get access token's metadata.
    """
    try:
        return _access_tokens.get(token)

    except _cache.error.KeyNotExist:
        raise _error.InvalidAccessToken('Invalid access token')


def generate_access_token(user: _model.AbstractUser) -> str:
    """Generate new access token.
    """
    with _threading.get_shared_r_lock():
        while True:
            token = _util.random_str(32)

            if not _access_tokens.has(token):
                now = _datetime.now()
                t_info = {
                    'user_uid': user.uid,
                    'ttl': _access_token_ttl,
                    'created': now,
                    'expires': now + _timedelta(seconds=_access_token_ttl),
                }
                _access_tokens.put(token, t_info, _access_token_ttl)

                return token


def revoke_access_token(token: str):
    if not token or not _access_tokens.has(token):
        raise _error.InvalidAccessToken('Invalid access token')

    with _threading.get_shared_r_lock():
        _access_tokens.rm(token)


def prolong_access_token(token: str):
    """Prolong user's access token.
    """
    with _threading.get_shared_r_lock():
        token_info = get_access_token_info(token)
        _access_tokens.put(token, token_info, _access_token_ttl)


def sign_out(user: _model.AbstractUser):
    """Sign out current user.
    """
    # Anonymous user cannot be signed out
    if user.is_anonymous:
        return

    # All operation on current user perform on behalf of system user
    switch_user_to_system()

    # Ask drivers to perform necessary operations
    for driver in _authentication_drivers.values():
        driver.sign_out(user)

    # Notify listeners
    _events.fire('pytsite.auth.sign_out', user=user)

    # Set anonymous user as current
    switch_user_to_anonymous()


def get_current_user() -> _model.AbstractUser:
    """Get current user.
    """
    user = _current_user.get(_threading.get_id())
    if user:
        return user

    return switch_user_to_anonymous()


def switch_user(user: _model.AbstractUser):
    """Switch current user.
    """
    tid = _threading.get_id()
    _previous_user[tid] = _current_user[tid] if tid in _current_user else get_anonymous_user()
    _current_user[tid] = user

    return user


def restore_user() -> _model.AbstractUser:
    """Switch to previous user.
    """
    tid = _threading.get_id()
    _current_user[tid] = _previous_user[tid] if tid in _previous_user else get_anonymous_user()

    return _current_user[tid]


def switch_user_to_system() -> _model.AbstractUser:
    """Shortcut.
    """
    return switch_user(get_system_user())


def switch_user_to_anonymous() -> _model.AbstractUser:
    """Shortcut.
    """
    return switch_user(get_anonymous_user())


def get_user_statuses() -> tuple:
    """Get valid user statuses.
    """
    return (
        ('active', _lang.t('pytsite.auth@status_active')),
        ('waiting', _lang.t('pytsite.auth@status_waiting')),
        ('disabled', _lang.t('pytsite.auth@status_disabled')),
    )


def get_sign_in_url(auth_driver_name: str = None, add_query: dict = None, add_fragment: str = None) -> str:
    """Get login URL.
    """
    # Get default authentication driver
    if not auth_driver_name:
        auth_driver_name = list(_authentication_drivers)[-1]

    return _router.ep_url('pytsite.auth@sign_in', {
        'driver': auth_driver_name,
        '__redirect': _router.current_url(add_query=add_query, add_fragment=add_fragment)
    })


def get_sign_out_url() -> str:
    """Get sign out URL.
    """
    return _router.ep_url('pytsite.auth@sign_out', {'__redirect': _router.current_url()})


def get_users(flt: dict = None, sort_field: str = None, sort_order: int = 1, limit: int = 0,
              skip: int = 0) -> _Iterable[_model.AbstractUser]:
    """Get users iterable.
    """
    return get_storage_driver().get_users(flt, sort_field, sort_order, limit, skip)


def get_roles(flt: dict = None, sort_field: str = None, sort_order: int = 1, limit: int = 0,
              skip: int = 0) -> _Iterable[_model.AbstractRole]:
    """Get roles iterable.
    """
    return get_storage_driver().get_roles(flt, sort_field, sort_order, limit, skip)


def count_users(flt: dict = None) -> int:
    """Count users.
    """
    return get_storage_driver().count_users(flt)


def count_roles(flt: dict = None) -> int:
    """Count roles.
    """
    return get_storage_driver().count_roles(flt)


def get_user_modify_form(user: _model.AbstractUser) -> _form.Form:
    """Get user modification form.
    """
    return get_storage_driver().get_user_modify_form(user)
