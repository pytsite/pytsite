"""Auth Console Commands.
"""
from getpass import getpass as _getpass
from pytsite import console as _console, lang as _lang
from . import _api, _error

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


class Passwd(_console.Command):
    """Abstract command.
    """

    @property
    def name(self) -> str:
        """Get command's name.
        """
        return 'auth:passwd'

    @property
    def description(self) -> str:
        """Get command's description.
        """
        return 'pytsite.auth@passwd_console_command_description'

    def exec(self):
        """Execute the command.
        """
        login = self.arg(0)

        try:
            user = _api.get_user(login)
        except _error.UserNotExist as e:
            raise _console.error.Error(_lang.t('pytsite.auth@user_is_not_exist', {'login': login}))

        pass_1 = _getpass(_lang.t('pytsite.auth@enter_new_password', {'login': user.login}) + ': ')
        if not pass_1:
            raise _console.error.Error(_lang.t('pytsite.auth@password_cannot_be_empty'))

        pass_2 = _getpass(_lang.t('pytsite.auth@retype_password') + ': ')

        if pass_1 != pass_2:
            raise _console.error.Error(_lang.t('pytsite.auth@passwords_dont_match'))

        try:
            _api.switch_user_to_system()
            user.password = pass_2
            user.save()
            _console.print_success(_lang.t('pytsite.auth@password_successfully_changed', {'login': user.login}))
        except Exception as e:
            raise _console.error.Error(str(e))
