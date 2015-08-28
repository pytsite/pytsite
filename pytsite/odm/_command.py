"""ODM Console Commands.
"""
__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


from pytsite import console as _console, lang as _lang, logger as _logger
from . import _functions


class RebuildIndices(_console.command.Abstract):
    """Cleanup All Command.
    """
    def get_name(self) -> str:
        """Get name of the command.
        """
        return 'odm:reindex'

    def get_description(self) -> str:
        """Get description of the command.
        """
        return _lang.t('pytsite.odm@reindex_console_command_description')

    def execute(self, **kwargs: dict):
        """Execute the command.
        """
        for model in _functions.get_registered_models():
            msg = _lang.t('pytsite.odm@reindex_model', {'model': model})
            _console.print_info(msg)
            _logger.info(msg, __name__)
            _functions.dispense(model).reindex()
