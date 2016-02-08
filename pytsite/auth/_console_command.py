"""Auth Console Commands.
"""
from getpass import getpass as _getpass
from pytsite import console as _console, lang as _lang
from . import _api

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


class Auth(_console.command.Abstract):
    """Abstract command.
    """
    def get_name(self) -> str:
        """Get command's name.
        """
        return 'auth'

    def get_description(self) -> str:
        """Get command's description.
        """
        return _lang.t('pytsite.auth@console_command_description')

    def get_help(self) -> str:
        """Get help for the command.
        """
        return '{} <passwd>'.format(self.get_name())

    def execute(self, args: tuple=(), **kwargs):
        """Execute teh command.
        """
        if len(args) != 1 or 'passwd' not in args:
            _console.print_info(self.get_help())
            return 1

        if 'passwd' in args:
            self._passwd(**kwargs)

    def _passwd(self, **kwargs):
        if 'login' not in kwargs:
            _console.print_info('{} passwd --login=<login>')
            return 1

        user = _api.get_user(kwargs['login'])
        if not user:
            raise _console.error.Error(_lang.t('pytsite.auth@user_is_not_exist', {'login': kwargs['login']}))

        pass_1 = _getpass(_lang.t('pytsite.auth@enter_new_password') + ': ')
        if not pass_1:
            raise _console.error.Error(_lang.t('pytsite.auth@password_cannot_be_empty'))

        pass_2 = _getpass(_lang.t('pytsite.auth@retype_password') + ': ')

        if pass_1 != pass_2:
            raise _console.error.Error(_lang.t('pytsite.auth@passwords_dont_match'))

        try:
            user.f_set('password', pass_2).save()
            _console.print_success(_lang.t('pytsite.auth@password_successfully_changed'))
        except Exception as e:
            raise _console.error.Error(str(e))
