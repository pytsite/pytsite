"""ODM Console Commands.
"""
from pytsite import console as _console, lang as _lang, logger as _logger, maintenance as _maintenance, \
    validation as _validation
from . import _api

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


class ODM(_console.command.Abstract):
    """Cleanup All Command.
    """
    def get_name(self) -> str:
        """Get name of the command.
        """
        return 'odm'

    def get_description(self) -> str:
        """Get description of the command.
        """
        return _lang.t('pytsite.odm@console_command_description')

    def get_options_help(self) -> str:
        """Get help for the command.
        """
        return '--reindex'

    def get_options(self) -> tuple:
        """Get command options.
        """
        return (
            ('reindex', _validation.rule.Pass()),
        )

    def _reindex(self):
        _maintenance.enable()

        for model in _api.get_registered_models():
            msg = _lang.t('pytsite.odm@reindex_model', {'model': model})
            _console.print_info(msg)
            _logger.info(msg, __name__)
            _api.dispense(model).reindex()

        _maintenance.disable()

    def execute(self, args: tuple=(), **kwargs):
        """Execute the command.
        """
        if not kwargs:
            raise _console.error.InsufficientArguments()

        for arg in kwargs:
            if arg == 'reindex':
                self._reindex()
