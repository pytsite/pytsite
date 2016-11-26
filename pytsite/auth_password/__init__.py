"""PytSite Password Authentication Driver Package.
"""

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


def _init():
    from pytsite import auth, lang
    from . import _driver

    lang.register_package(__name__)
    auth.register_auth_driver(_driver.Password())


_init()
