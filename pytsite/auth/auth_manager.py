"""Auth Manager.
"""
__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

from werkzeug.security import generate_password_hash, check_password_hash
from pytsite.core import router, forms, odm
from pytsite.core.lang import t
from .errors import *
from .models import User, Role
from .drivers.abstract import AbstractDriver

__driver = None
__permission_groups = []
__permissions = []
__anonymous_user = None


def password_hash(secret: str) -> str:
    """Hash string.
    """
    return generate_password_hash(secret)


def password_verify(clear_text: str, hashed: str) -> bool:
    """Verify hashed string.
    """
    return check_password_hash(hashed, clear_text)


def set_driver(driver: AbstractDriver):
    """Change current driver.
    """
    if not isinstance(driver, AbstractDriver):
        raise TypeError('Instance of AbstractDriver expected.')

    global __driver
    __driver = driver


def get_driver() -> AbstractDriver:
    """Get current driver.
    """
    if not __driver:
        raise Exception("No driver selected.")

    return __driver


def get_permission_group(name: str) -> tuple:
    """Get permission group spec.
    """
    for group in __permission_groups:
        if group[0] == name:
            return group


def define_permission_group(name: str, description: str):
    """Define permission group.
    """
    if get_permission_group(name):
        raise KeyError("Permission group '{}' is already defined.".format(name))

    __permission_groups.append((name, description))


def get_permission_groups() -> list:
    """Get all defined permission groups.
    """
    return __permission_groups


def get_permission(name: str) -> tuple:
    """Get permission spec.
    """
    for perm in __permissions:
        if perm[0] == name:
            return perm


def is_permission_defined(name: str) -> bool:
    """Checks if the permission is defined.
    """
    return bool(get_permission(name))


def define_permission(name: str, description: str, group: str):
    """Define permission.
    """
    if not get_permission_group(group):
        raise KeyError("Permission group '{}' is not defined.".format(group))

    if get_permission(name):
        raise ValueError("Permission '{0}' is already defined.".format(name))

    __permissions.append((name, description, group))


def get_permissions(group: str=None) -> list:
    """Get all defined permissions.
    """
    r = []
    for perm in __permissions:
        if group and perm[2] != group:
            continue
        r.append(perm)

    return r


def get_login_form(uid: str=None) -> forms.BaseForm:
    """Get a login form.
    """
    if not uid:
        uid = 'auth-form'

    form = get_driver().get_login_form(uid)
    form.action = router.endpoint_url('pytsite.auth.eps.post_login')

    return form


def post_login_form(args: dict, inp: dict) -> router.RedirectResponse:
    """Post a login form.
    """
    return get_driver().post_login_form(args, inp)


def create_user(email: str, login: str=None, password: str=None) -> User:
    """Create new user.
    """

    if not login:
        login = email

    if get_user(login=login):
        raise Exception("User with login '{0}' already exists.".format(login))

    user = odm.odm_manager.dispense('user')
    user.f_set('login', login).f_set('email', email)

    if password:
        user.f_set('password', password)

    return user


def get_user(login: str=None, uid: str=None) -> User:
    """Get user by login.
    """

    if login:
        return odm.odm_manager.find('user').where('login', '=', login).first()
    if uid:
        return odm.odm_manager.find('user').where('_id', '=', uid).first()


def create_role(name: str, description: str=''):
    if get_role(name=name):
        raise Exception("Role with name '{0}' already exists.".format(name))

    role = odm.odm_manager.dispense('role')
    return role.f_set('name', name).f_set('description', description)


def get_role(name: str=None, uid=None) -> Role:
    if name:
        return odm.odm_manager.find('role').where('name', '=', name).first()
    if uid:
        return odm.odm_manager.find('role').where('_id', '=', uid).first()


def authorize(user: User)->User:
    """Authorize user.
    """

    if not user:
        raise LoginIncorrect('pytsite.auth@authorization_error')

    if user.f_get('status') != 'active':
        logout_current_user()
        raise LoginIncorrect('pytsite.auth@authorization_error')

    router.session['pytsite.auth.login'] = user.f_get('login')

    return user


def get_anonymous_user() -> User:
    """Get anonymous user.
    """

    global __anonymous_user
    if not __anonymous_user:
        __anonymous_user = create_user('__anonymous@nowhere.com', '__anonymous')

    return __anonymous_user


def get_current_user() -> User:
    """Get currently authorized user.
    """

    login = router.session.get('pytsite.auth.login')
    if not login:
        return get_anonymous_user()

    try:
        user = get_user(login=login)
        if not user:
            return get_anonymous_user()

        return authorize(user)

    except LoginIncorrect:
        return get_anonymous_user()


def logout_current_user():
    """Log out current user.
    """

    if 'pytsite.auth.login' in router.session:
        del router.session['pytsite.auth.login']


def get_user_statuses() -> list:
    """Get available user statuses.
    """

    return [
        ('active', t('pytsite.auth@status_active')),
        ('waiting', t('pytsite.auth@status_waiting')),
        ('disabled', t('pytsite.auth@status_disabled')),
    ]
