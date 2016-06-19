"""PytSite Auth Password Driver Package.
"""

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


def _init():
    from pytsite import auth
    from . import _driver

    auth.register_auth_driver(_driver.Password())

_init()
