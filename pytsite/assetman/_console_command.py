"""PytSite Assetman Console Commands.
"""
from pytsite import console as _console, validation as _validation
from . import _api

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


class Assetman(_console.command.Abstract):
    """assetman:build Console Command.
    """

    def get_name(self) -> str:
        """Get name of the command.
        """
        return 'assetman'

    def get_description(self) -> str:
        """Get description of the command.
        """
        from pytsite.lang import t
        return t('pytsite.assetman@assetman_console_command_description')

    def get_options_help(self) -> str:
        """Get help for the command.
        """
        return '--build [--no-maintenance]'

    def get_options(self) -> tuple:
        """Get command options.
        """
        return (
            ('build', _validation.rule.Pass()),
            ('no-maintenance', _validation.rule.Pass()),
        )

    def execute(self, args: tuple = (), **kwargs):
        """Execute The Command.
        """
        if not kwargs:
            return _console.run_command('help', ('assetman',))

        if 'build' in kwargs:
            _api.build(maintenance=not kwargs.get('no-maintenance', False))
