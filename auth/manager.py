"""Auth service.
"""

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


from ..core.router import RedirectResponse
from ..core.form import AbstractForm
from .models import User
from .drivers.abstract import AbstractDriver


__driver = None


def set_driver(driver: AbstractDriver):
    """Change current driver.
    """
    if not isinstance(driver, AbstractDriver):
        raise TypeError('Instance of AbstractDriver expected.')
    global __driver
    __driver = driver


def get_driver()->AbstractDriver:
    global __driver
    if not __driver:
        raise Exception("No driver selected.")
    return __driver


def get_login_form()->AbstractForm:
    """Get a login form.
    """
    return get_driver().get_login_form()


def post_login_form(args: dict, inp: dict)->RedirectResponse:
    """Post a login form.
    """
    return get_driver().post_login_form(args, inp)


def create_user(login: str, email: str)->User:
    """Create new user.
    """
    from ..core import odm, utils

    user = odm.manager.dispense('user')
    user.f_set('login', login).f_set('email', email).f_set('password', utils.random_password())

    return user


def get_user_by_login(login: str)->User:
    """Get user by login.
    """
    from ..core import odm
    return odm.manager.find('user').where('login', '=', login).first()