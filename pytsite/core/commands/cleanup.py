"""Cleanup console command.
"""
__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

from os import listdir, path, unlink
from time import time
from .. import console, lang, reg


class CleanupAllCommand(console.AbstractCommand):
    """Cleanup All Command.
    """

    def get_name(self) -> str:
        """Get name of the command.
        """

        return 'app:cleanup'

    def get_description(self) -> str:
        """Get description of the command.
        """

        return lang.t('pytsite.core@cleanup_all_console_command_description')

    def execute(self, **kwargs: dict):
        """Execute the command.
        """

        console.run_command('cleanup:tmp', **kwargs)
        console.run_command('cleanup:session', **kwargs)


class CleanupTmpCommand(console.AbstractCommand):
    def get_name(self) -> str:
        return 'app:cleanup:tmp'

    def get_description(self):
        return lang.t('pytsite.core@cleanup_tmp_console_command_description')

    def execute(self, **kwargs: dict):
        tmp_dir = reg.get('paths.tmp')
        for file_name in listdir(tmp_dir):
            file_path = path.join(tmp_dir, file_name)
            if path.isfile(file_path):
                unlink(file_path)


class CleanupSessionCommand(console.AbstractCommand):
    def get_name(self) -> str:
        return 'app:cleanup:session'

    def get_description(self):
        return lang.t('pytsite.core@cleanup_session_console_command_description')

    def execute(self, **kwargs: dict):
        session_dir = reg.get('paths.session')
        ttl = int(reg.get('session.ttl', 21600))  # 6 hours
        for file_name in listdir(session_dir):
            file_path = path.join(session_dir, file_name)
            if path.isfile(file_path) and (time() - path.getmtime(file_path)) >= ttl:
                unlink(file_path)
