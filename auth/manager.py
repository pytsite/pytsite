"""Auth Manager.
"""
__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from pytsite.core import router, forms, odm, lang
from .errors import *
from .models import User
from .drivers.abstract import AbstractDriver

__driver = None
__permissions = {}


def password_hash(secret: str)->str:
    """Hash string with SHA-512.
    """
    return generate_password_hash(secret)


def password_verify(secret: str, hashed: str)->bool:
    """Verify SHA-512 hashed string.
    """
    return check_password_hash(hashed, secret)


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
    return __permissions


def get_login_form()->forms.AbstractForm:
    """Get a login form.
    """
    return get_driver().get_login_form()


def post_login_form(args: dict, inp: dict)->router.RedirectResponse:
    """Post a login form.
    """
    return get_driver().post_login_form(args, inp)


def create_user(email: str, login: str=None, password: str=None)->User:
    """Create new user.
    """
    if not login:
        login = email

    if get_user(login=login):
        raise Exception("User with login '{0}' already exists.".format(login))

    user = odm.manager.dispense('user')
    user.f_set('login', login).f_set('email', email)

    if password:
        user.f_set('password', password)

    return user


def get_user(login: str=None, uid: str=None)->User:
    """Get user by login.
    """
    if login:
        return odm.manager.find('user').where('login', '=', login).first()
    if uid:
        return odm.manager.find('user').where('_id', '=', uid).first()


def authorize(user: User):
    if not user:
        raise LoginIncorrect('pytsite.auth@authorization_error')

    if user.f_get('status') != 'active':
        raise LoginIncorrect('pytsite.auth@authorization_error')

    user.f_add('loginCount', 1).f_set('lastLogin', datetime.now()).save()

    router.session['pytsite.auth.login'] = user.f_get('login')