__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

from datetime import datetime
from os import path
from .. import console, lang, events, reg


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

        # Is setup already completed?
        lock_path = reg.get('paths.setup.lock')
        if path.exists(lock_path):
            raise Exception(lang.t('pytsite.auth@setup_already_completed'))

        events.fire('app.setup')

        # Writing lock file
        with open(lock_path, 'wt') as f:
            f.write(datetime.now().isoformat())
