"""PytSite Assetman Console Commands.
"""
from pytsite import console as _console, validation as _validation
from . import _api, _error

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


class Build(_console.command.Abstract):
    """assetman:build Console Command.
    """

    def get_name(self) -> str:
        """Get name of the command.
        """
        return 'assetman:build'

    def get_description(self) -> str:
        """Get description of the command.
        """
        from pytsite.lang import t
        return t('pytsite.assetman@assetman_console_command_description')

    def get_options_help(self) -> str:
        """Get help for the command.
        """
        return '[--package=NAME] [--no-maint] [--no-cache]'

    def get_options(self) -> tuple:
        """Get command options.
        """
        return (
            ('package', _validation.rule.Pass()),
            ('no-maint', _validation.rule.Pass()),
            ('no-cache', _validation.rule.Pass()),
        )

    def execute(self, args: tuple = (), **kwargs):
        """Execute The Command.
        """
        try:
            _api.build(kwargs.get('package'), not kwargs.get('no-maint'), not kwargs.get('no-cache'))

        except (_error.PackageNotRegistered, _error.PackageAlreadyRegistered) as e:
            raise _console.error.Error(e)
