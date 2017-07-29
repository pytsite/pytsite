"""PytSite Auth HTTP Related Functions
"""
from pytsite import auth as _auth, form as _form, router as _router, lang as _lang, reg as _reg

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


def base_path() -> str:
    return _reg.get('auth.routes_base_path', '/auth')


def sign_in_form(driver_name: str = None, **kwargs) -> _form.Form:
    """Get a login form
    """
    driver = _auth.get_auth_driver(driver_name)

    kwargs.update({
        'name': kwargs.get('name', 'pytsite-auth-sign-in-' + driver.name),
        'css': kwargs.get('css', '') + ' pytsite-auth-sign-in driver-' + driver.name
    })

    form = driver.get_sign_in_form(**kwargs)
    form.action = _router.rule_url('pytsite.auth_web@sign_in_submit', {'driver': driver.name})

    if not form.title:
        form.title = _lang.t('pytsite.auth_web@authentication')

    return form


def user_modify_form(user: _auth.model.AbstractUser) -> _form.Form:
    """Get user modification form
    """
    return _auth.get_storage_driver().get_user_modify_form(user)


def sign_in_url(auth_driver_name: str = None, add_query: dict = None, add_fragment: str = None) -> str:
    """Get login URL
    """
    # Get default authentication driver
    if not auth_driver_name:
        auth_driver_name = _auth.get_auth_driver().name

    return _router.rule_url('pytsite.auth_web@sign_in', {
        'driver': auth_driver_name,
        '__redirect': _router.current_url(add_query=add_query, add_fragment=add_fragment)
    })


def sign_out_url() -> str:
    """Get sign out URL
    """
    return _router.rule_url('pytsite.auth_web@sign_out', {'__redirect': _router.current_url()})
