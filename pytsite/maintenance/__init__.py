"""PytSite Maintenance Package.
"""
# Public API
from ._api import enable, disable, is_enabled

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


def _init():
    from pytsite import console, lang
    from . import _command

    lang.register_package(__name__)
    console.register_command(_command.Maintenance())


_init()
