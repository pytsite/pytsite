"""PytSite Cleanup Console Commands.
"""
__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

import time as _time
from os import listdir as _listdir, path as _path, unlink as _unlink
from pytsite import console as _console, reg as _reg


class Cleanup(_console.command.Abstract):
    """Cleanup All Command.
    """
    def get_name(self) -> str:
        """Get name of the command.
        """
        return 'app:cleanup'

    def get_description(self) -> str:
        """Get description of the command.
        """
        from pytsite.lang import t
        return t('pytsite.cleanup@cleanup_all_console_command_description')

    def execute(self, **kwargs: dict):
        """Execute the command.
        """
        _console.run_command('cleanup:tmp', **kwargs)
        _console.run_command('cleanup:session', **kwargs)


class CleanupTmpFiles(_console.command.Abstract):
    """Cleanup Tmp Files Command.
    """
    def get_name(self) -> str:
        return 'app:cleanup:tmp'

    def get_description(self):
        from pytsite.lang import t
        return t('pytsite.cleanup@cleanup_tmp_console_command_description')

    def execute(self, **kwargs: dict):
        tmp_dir = _reg.get('paths.tmp')
        for file_name in _listdir(tmp_dir):
            file_path = _path.join(tmp_dir, file_name)
            if _path.isfile(file_path):
                _unlink(file_path)


class CleanupOldSessions(_console.command.Abstract):
    """Cleanup Old Session Files Command.
    """
    def get_name(self) -> str:
        return 'app:cleanup:session'

    def get_description(self):
        from pytsite.lang import t
        return t('pytsite.cleanup@cleanup_session_console_command_description')

    def execute(self, **kwargs: dict):
        session_dir = _reg.get('paths.session')
        ttl = int(_reg.get('session.ttl', 21600))  # 6 hours
        for file_name in _listdir(session_dir):
            file_path = _path.join(session_dir, file_name)
            if _path.isfile(file_path) and (_time.time() - _path.getmtime(file_path)) >= ttl:
                _unlink(file_path)
