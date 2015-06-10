__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

from datetime import datetime
from os import path, makedirs
from .. import console, lang, events, reg, errors


class SetupCommand(console.AbstractCommand):
    """Setup Command.
    """

    def get_name(self) -> str:
        """Get name of the command.
        """
        return 'app:setup'

    def get_description(self) -> str:
        """Get description of the command.
        """
        return lang.t('pytsite.core@setup_console_command_description')

    def execute(self, **kwargs: dict):
        """Execute the command.
        """
        lock_path = reg.get('paths.setup.lock')
        if path.exists(lock_path):
            raise errors.ConsoleRuntimeError(lang.t('pytsite.auth@setup_already_completed'))

        events.fire('app.setup')

        # Writing lock file
        lock_dir = path.dirname(lock_path)
        if not path.isdir(lock_dir):
            makedirs(lock_dir, 0o755, True)
        with open(lock_path, 'wt') as f:
            f.write(datetime.now().isoformat())

        console.print_info(lang.t('pytsite.core@setup_has_been_completed'))