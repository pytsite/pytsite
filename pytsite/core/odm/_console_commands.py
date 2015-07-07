"""ODM Console Commands.
"""
__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


from pytsite.core import console as _console, lang as _lang
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
        return _lang.t('core.odm@reindex_console_command_description')

    def execute(self, **kwargs: dict):
        """Execute the command.
        """
        for model in _functions.get_registered_models():
            mock = _functions.dispense(model)
            mock.reindex()
            _console.print_success(_lang.t('core.odm@reindex_model', {'model': model}))
