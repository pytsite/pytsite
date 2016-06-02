"""PytSite uLogin Package.
"""

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


def _init():
    from pytsite import auth, tpl, assetman
    from ._auth_driver import ULogin

    auth.register_driver(ULogin())
    tpl.register_package(__name__)
    assetman.register_package(__name__)


_init()
