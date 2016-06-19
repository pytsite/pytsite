"""PytSite Auth Google Driver.
"""

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


def _init():
    from pytsite import auth, lang, assetman
    from . import _driver

    lang.register_package(__name__)
    assetman.register_package(__name__)
    auth.register_auth_driver(_driver.Google())

_init()
