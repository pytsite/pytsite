"""PytSite Setup Console Command
"""
from datetime import datetime as _datetime
from os import path as _path, makedirs as _makedirs
from pytsite import console as _console, reg as _reg, events as _events, lang as _lang, validation as _validation

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


class Setup(_console.command.Abstract):
    """Setup Console Command
    """
    def get_name(self) -> str:
        """Get name of the command.
        """
        return 'setup'

    def get_description(self) -> str:
        """Get description of the command.
        """
        from pytsite.lang import t
        return t('pytsite.setup@setup_console_command_description')

    def get_options_help(self) -> str:
        """Get help for the command.
        """
        return '[--force]'

    def get_options(self) -> tuple:
        return (
            ('force', _validation.rule.Pass()),
        )

    def execute(self, args: tuple=(), **kwargs):
        """Execute the command.
        """
        lock_path = _reg.get('paths.setup.lock')
        if _path.exists(lock_path) and not kwargs.get('force'):
            raise _console.error.Error(_lang.t('pytsite.setup@setup_is_already_completed'))

        _events.fire('pytsite.setup')

        # Writing lock file
        lock_dir = _path.dirname(lock_path)
        if not _path.isdir(lock_dir):
            _makedirs(lock_dir, 0o755, True)
        with open(lock_path, 'wt') as f:
            f.write(_datetime.now().isoformat())

        _console.print_info(_lang.t('pytsite.setup@setup_has_been_completed'))

        # Run 'update' to build updates info file
        _console.run_command('update', stage=2)
