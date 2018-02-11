"""PytSite pip Support
"""

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

# Public API
from . import _error as error
from ._api import get_installed_info, get_installed_version, is_installed, install, uninstall


def _init():
    from pytsite import lang, console, update
    from . import _cc, _eh

    # Resource packages
    lang.register_package(__name__)

    # Console commands
    console.register_command(_cc.Install())
    console.register_command(_cc.Uninstall())

    # Events handlers
    update.on_update_stage_2(_eh.update_stage_2)

_init()
