"""PytSite Setup Console Command
"""
from datetime import datetime as _datetime
from os import path as _path, makedirs as _makedirs
from pytsite import console as _console, reg as _reg, events as _events, lang as _lang

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


class Setup(_console.Command):
    """Setup Console Command
    """

    def __init__(self):
        super().__init__()

        self.define_option(_console.option.Bool('force'))

    @property
    def name(self) -> str:
        """Get name of the command.
        """
        return 'setup'

    @property
    def description(self) -> str:
        """Get description of the command.
        """
        return 'pytsite.setup@setup_console_command_description'

    def exec(self):
        """Execute the command.
        """
        lock_path = _reg.get('paths.setup.lock')
        if _path.exists(lock_path) and not self.opt('force'):
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
        _console.run_command('update', {'stage': 2})
