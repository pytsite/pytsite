"""Core Console Commands
"""
__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

import pickle
from abc import ABC, abstractmethod
from datetime import datetime
from os import listdir, path, unlink, makedirs
from time import time
from pytsite.core import reg, events
from . import _error


class Abstract(ABC):
    """Abstract command.
    """

    @abstractmethod
    def get_name(self) -> str:
        pass

    @abstractmethod
    def get_description(self) -> str:
        pass

    @abstractmethod
    def execute(self, **kwargs: dict):
        pass


class Cleanup(Abstract):
    """Cleanup All Command.
    """

    def get_name(self) -> str:
        """Get name of the command.
        """
        return 'app:cleanup'

    def get_description(self) -> str:
        """Get description of the command.
        """
        from pytsite.core.lang import t
        return t('pytsite.core@cleanup_all_console_command_description')

    def execute(self, **kwargs: dict):
        """Execute the command.
        """
        from ._functions import run_console_command
        run_console_command('cleanup:tmp', **kwargs)
        run_console_command('cleanup:session', **kwargs)


class CleanupTmpFiles(Abstract):
    """Cleanup Tmp Files Command.
    """

    def get_name(self) -> str:
        return 'app:cleanup:tmp'

    def get_description(self):
        from pytsite.core.lang import t
        return t('pytsite.core@cleanup_tmp_console_command_description')

    def execute(self, **kwargs: dict):
        tmp_dir = reg.get('paths.tmp')
        for file_name in listdir(tmp_dir):
            file_path = path.join(tmp_dir, file_name)
            if path.isfile(file_path):
                unlink(file_path)


class CleanupOldSessions(Abstract):
    """Cleanup Old Session Files Command.
    """

    def get_name(self) -> str:
        return 'app:cleanup:session'

    def get_description(self):
        from pytsite.core.lang import t
        return t('pytsite.core@cleanup_session_console_command_description')

    def execute(self, **kwargs: dict):
        session_dir = reg.get('paths.session')
        ttl = int(reg.get('session.ttl', 21600))  # 6 hours
        for file_name in listdir(session_dir):
            file_path = path.join(session_dir, file_name)
            if path.isfile(file_path) and (time() - path.getmtime(file_path)) >= ttl:
                unlink(file_path)


class Cron(Abstract):
    """Cron command.
    """
    def get_name(self):
        """Get command name.
        """
        return 'cron:start'

    def get_description(self):
        """Get command description.
        """
        from pytsite.core.lang import t
        return t('pytsite.core@cron_console_command_description')

    def execute(self, **kwargs: dict):
        """Execute the command.
        """
        lock_path = self._get_lock_file_path()
        if path.exists(lock_path):
            raise Exception('Lock file exists.')

        self._lock_file_op(True)

        d = self._get_descriptor()
        now = datetime.now()
        for evt in 'hourly', 'daily', 'weekly', 'monthly':
            delta = now - d[evt]
            if evt == 'hourly' and delta.total_seconds() >= 3600\
                    or evt == 'daily' and delta.total_seconds() >= 86400\
                    or evt == 'weekly' and delta.total_seconds() >= 604800\
                    or evt == 'monthly' and delta.total_seconds() >= 2592000:
                events.fire(__name__ + '@' + evt)
                self._update_descriptor(evt)

        self._lock_file_op(False)

    def _get_descriptor_file_path(self):
        """Get descriptor file path.
        """

        return path.join(reg.get('paths.storage'), 'cron.data')

    def _get_lock_file_path(self) -> str:
        """Get lock file path.
        """
        return path.join(reg.get('paths.storage'), 'cron.lock')

    def _lock_file_op(self, op: bool):
        """Operation with lock file.
        """
        file_path = self._get_lock_file_path()
        if op:
            with open(file_path, 'wt') as f:
                f.write(datetime.now().isoformat())
        elif path.exists(file_path):
            unlink(file_path)

    def _get_descriptor(self) -> dict:
        """Get descriptor info.
        """
        data = None
        file_path = self._get_descriptor_file_path()
        if not path.exists(file_path):
            data = {
                'hourly': datetime.fromtimestamp(0),
                'daily': datetime.fromtimestamp(0),
                'weekly': datetime.fromtimestamp(0),
                'monthly': datetime.fromtimestamp(0),
            }
            with open(file_path, 'wb') as f:
                pickle.dump(data, f)
            return data
        else:
            with open(file_path, 'rb') as f:
                data = pickle.load(f)

        return data

    def _update_descriptor(self, part: str) -> dict:
        """Update descriptor.
        """
        data = self._get_descriptor()
        data[part] = datetime.now()
        with open(self._get_descriptor_file_path(), 'wb') as f:
            pickle.dump(data, f)

        return data


class Setup(Abstract):
    """Setup Command.
    """

    def get_name(self) -> str:
        """Get name of the command.
        """
        return 'app:setup'

    def get_description(self) -> str:
        """Get description of the command.
        """
        from pytsite.core.lang import t
        return t('pytsite.core@setup_console_command_description')

    def execute(self, **kwargs: dict):
        """Execute the command.
        """
        from pytsite.core.lang import t

        lock_path = reg.get('paths.setup.lock')
        if path.exists(lock_path):
            raise _error.ConsoleRuntimeError(t('pytsite.core@setup_already_completed'))

        events.fire('app.setup')

        # Writing lock file
        lock_dir = path.dirname(lock_path)
        if not path.isdir(lock_dir):
            makedirs(lock_dir, 0o755, True)
        with open(lock_path, 'wt') as f:
            f.write(datetime.now().isoformat())

        from ._functions import print_info
        print_info(t('pytsite.core@setup_has_been_completed'))
