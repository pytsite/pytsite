"""PytSite uLogin Package.
"""

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


def _init():
    from pytsite import auth, tpl, assetman, lang
    from ._driver import ULogin

    auth.register_auth_driver(ULogin())
    lang.register_package(__name__)
    tpl.register_package(__name__)
    assetman.register_package(__name__)


_init()
