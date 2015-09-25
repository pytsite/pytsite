"""PytSite Setup Console Commands.
"""
__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

from pytsite import console as _console
from datetime import datetime as _datetime
from os import path as _path, makedirs as _makedirs
from pytsite import reg as _reg, events as _events, lang as _lang


class Setup(_console.command.Abstract):
    """Setup Command.
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

    def execute(self, **kwargs: dict):
        """Execute the command.
        """
        lock_path = _reg.get('paths.setup.lock')
        if _path.exists(lock_path):
            raise _console.Error(_lang.t('pytsite.setup@setup_is_already_completed'))

        _events.fire('pytsite.setup')

        # Writing lock file
        lock_dir = _path.dirname(lock_path)
        if not _path.isdir(lock_dir):
            _makedirs(lock_dir, 0o755, True)
        with open(lock_path, 'wt') as f:
            f.write(_datetime.now().isoformat())

        _console.print_info(_lang.t('pytsite.setup@setup_has_been_completed'))

        _console.run_command('update')
