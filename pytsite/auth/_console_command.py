"""Auth Console Commands.
"""
from getpass import getpass as _getpass
from pytsite import console as _console, lang as _lang, validation as _validation
from . import _api

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


class Passwd(_console.command.Abstract):
    """Abstract command.
    """
    def get_name(self) -> str:
        """Get command's name.
        """
        return 'auth:passwd'

    def get_description(self) -> str:
        """Get command's description.
        """
        return _lang.t('pytsite.auth@passwd_console_command_description')

    def get_options_help(self) -> str:
        """Get help for the command.
        """
        return '--login=<login>'

    def get_options(self) -> tuple:
        """Get command options.
        """
        return (
            ('login', _validation.rule.NonEmpty(msg_id='pytsite.auth@login_required')),
        )

    def execute(self, args: tuple=(), **kwargs):
        """Execute teh command.
        """
        user = _api.get_user(kwargs['login'])
        if not user:
            raise _console.error.Error(_lang.t('pytsite.auth@user_is_not_exist', {'login': kwargs['login']}))

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
