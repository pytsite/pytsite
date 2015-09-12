"""PytSite Auth Log Events Handlers.
"""
from pytsite import auth as _auth, odm as _odm, router as _router

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


def auth_login(user: _auth.model.User):
    """'pytsite.auth.login' event handler.
    """
    _create_odm_entity(user, 'pytsite.auth_log@login')


def auth_logout(user: _auth.model.User):
    """'pytsite.auth.logout' event handler.
    """
    _create_odm_entity(user, 'pytsite.auth_log@logout')


def _create_odm_entity(user: _auth.model.User, description: str):
    e = _odm.dispense('auth_log')
    e.f_set('user', user)
    e.f_set('ip', _router.request.remote_addr)
    e.f_set('description', description)
    e.save()
    return e