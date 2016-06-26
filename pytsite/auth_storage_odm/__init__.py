"""PytSIte Authentication ODM Storage Driver.
"""
from . import _model as model
from ._driver import Driver

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


def _init():
    from pytsite import odm, lang

    # Resources
    lang.register_package(__name__)

    # ODM models
    odm.register_model('user', model.User)
    odm.register_model('role', model.Role)

_init()
