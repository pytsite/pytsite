"""PytSite Authentication and Authorization
"""
# Public API
from . import _error as error, _model as model, _driver as driver
from ._api import get_current_user, get_user_statuses, get_user, create_user, get_role, register_auth_driver, \
    user_nickname_rule, sign_in, get_auth_driver, create_role, verify_password, hash_password, sign_out, \
    get_access_token_info, switch_user, get_anonymous_user, get_system_user, get_users, get_storage_driver, \
    count_users, count_roles, get_first_admin_user, get_roles, switch_user_to_system, switch_user_to_anonymous, \
    restore_user, generate_access_token, prolong_access_token, register_storage_driver, get_auth_drivers

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


def _init():
    """Init wrapper
    """
    from pytsite import lang, console, permissions, setup
    from . import _eh, _console_commands

    # Resources
    lang.register_package(__name__)

    # Module permission group
    permissions.define_group('security', 'pytsite.auth@security')

    # Event handlers
    setup.on_setup(_eh.setup)

    # Console commands
    console.register_command(_console_commands.Passwd())


_init()
