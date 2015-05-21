"""Auth Manager.
"""
__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from pytsite.core import router, form, odm
from .errors import *
from .models import User, Role, AnonymousUser
from .drivers.abstract import AbstractDriver

__driver = None
__permissions = {}


def password_hash(secret: str)->str:
    """Hash string.
    """

    return generate_password_hash(secret)


def password_verify(clear_text: str, hashed: str)->bool:
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


def get_driver()->AbstractDriver:
    """Get current driver.
    """

    global __driver
    if not __driver:
        raise Exception("No driver selected.")

    return __driver


def define_permission(name: str, description: str=None):
    """Define permission.
    """

    global __permissions
    if name in __permissions:
        raise ValueError("Permission '{0}' already defined.")

    __permissions[name] = description


def get_permissions()->dict:
    """Get all defined permissions.
    """

    global __permissions
    return __permissions


def is_permission_defined(name: str) -> bool:
    """Checks if the permission is defined.
    """

    global __permissions
    return name in __permissions

def get_login_form(uid: str=None) -> form.AbstractForm:
    """Get a login form.
    """

    if not uid:
        uid = 'auth-form'

    form = get_driver().get_login_form(uid)
    form.action = router.endpoint_url('pytsite.auth.endpoints.post_login')

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

    user = odm.odm.dispense('user')
    user.f_set('login', login).f_set('email', email)

    if password:
        user.f_set('password', password)

    return user


def get_user(login: str=None, uid: str=None) -> User:
    """Get user by login.
    """

    if login:
        return odm.odm.find('user').where('login', '=', login).first()
    if uid:
        return odm.odm.find('user').where('_id', '=', uid).first()


def create_role(name: str, description: str=''):
    if get_role(name=name):
        raise Exception("Role with name '{0}' already exists.".format(name))

    role = odm.odm.dispense('role')
    return role.f_set('name', name).f_set('description', description)


def get_role(name: str=None, uid=None) -> Role:
    if name:
        return odm.odm.find('role').where('name', '=', name).first()
    if uid:
        return odm.odm.find('role').where('_id', '=', uid).first()


def authorize(user: User)->User:
    """Authorize user.
    """

    if not user:
        raise LoginIncorrect('pytsite.auth@authorization_error')

    if user.f_get('status') != 'active':
        logout_current_user()
        raise LoginIncorrect('pytsite.auth@authorization_error')

    user.f_add('loginCount', 1).f_set('lastLogin', datetime.now()).save()

    router.session['pytsite.auth.login'] = user.f_get('login')

    return user


def get_current_user() -> User:
    """Get currently authorized user.
    """

    login = router.session.get('pytsite.auth.login')
    if not login:
        return AnonymousUser()

    try:
        user = get_user(login=login)
        if not user:
            return AnonymousUser()

        return authorize(user)

    except LoginIncorrect:
        return None


def logout_current_user():
    """Log out current user.
    """

    if 'pytsite.auth.login' in router.session:
        del router.session['pytsite.auth.login']
