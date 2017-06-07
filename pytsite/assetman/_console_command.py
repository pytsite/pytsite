"""PytSite Assetman Console Commands
"""
from pytsite import console as _console, lang as _lang, maintenance as _maintenance
from . import _api, _error

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


class Setup(_console.Command):
    """assetman:setup Console Command.
    """

    @property
    def name(self) -> str:
        """Get name of the command.
        """
        return 'assetman:setup'

    @property
    def description(self) -> str:
        """Get description of the command.
        """
        return 'pytsite.assetman@assetman_setup_console_command_description'

    def execute(self, args: tuple = (), **kwargs):
        """Execute The Command.
        """
        try:
            _api.setup()
        except RuntimeError as e:
            raise _console.error.Error(e)


class Build(_console.Command):
    """assetman:build Console Command.
    """
    def __init__(self):
        super().__init__()

        self._define_option(_console.option.Bool('no-maint'))
        self._define_option(_console.option.Str('package'))

    @property
    def name(self) -> str:
        """Get name of the command.
        """
        return 'assetman:build'

    @property
    def description(self) -> str:
        """Get description of the command.
        """
        return 'pytsite.assetman@assetman_build_console_command_description'

    def execute(self):
        """Execute The Command.
        """
        maint = not self.get_option_value('no-maint')

        try:
            if maint:
                _maintenance.enable()

            # Compile assets
            _api.build(self.get_option_value('package'))

            # Compile translations
            _lang.build()

        except (RuntimeError, _error.PackageNotRegistered, _error.PackageAlreadyRegistered) as e:
            raise _console.error.Error(e)

        finally:
            if maint:
                _maintenance.disable()
