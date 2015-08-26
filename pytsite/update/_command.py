"""PytSite Update Console Commands.
"""
__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

from pytsite import console as _console, events as _events, lang as _lang, maintenance as _maintenance


class Update(_console.command.Abstract):
    """Setup Command.
    """
    def get_name(self) -> str:
        """Get name of the command.
        """
        return 'update'

    def get_description(self) -> str:
        """Get description of the command.
        """
        return _lang.t('pytsite.update@update_console_command_description')

    def execute(self, **kwargs: dict):
        """Execute the command.
        """
        _console.run_command('maintenance', enable=True)
        _events.fire('pytsite.update')
        _console.run_command('maintenance', disable=True)
