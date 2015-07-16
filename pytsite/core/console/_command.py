"""Console Commands
"""
__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

import pickle
from abc import ABC as _ABC, abstractmethod as _abstractmethod
from datetime import datetime as _datetime
from os import listdir as _listdir, path as _path, unlink as _unlink, makedirs as _makedirs
from time import time as _time
from pytsite.core import reg as _reg, events as _events
from . import _error


class Abstract(_ABC):
    """Abstract command.
    """
    @_abstractmethod
    def get_name(self) -> str:
        pass

    @_abstractmethod
    def get_description(self) -> str:
        pass

    @_abstractmethod
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
        from ._functions import run_command
        run_command('cleanup:tmp', **kwargs)
        run_command('cleanup:session', **kwargs)


class CleanupTmpFiles(Abstract):
    """Cleanup Tmp Files Command.
    """
    def get_name(self) -> str:
        return 'app:cleanup:tmp'

    def get_description(self):
        from pytsite.core.lang import t
        return t('pytsite.core@cleanup_tmp_console_command_description')

    def execute(self, **kwargs: dict):
        tmp_dir = _reg.get('paths.tmp')
        for file_name in _listdir(tmp_dir):
            file_path = _path.join(tmp_dir, file_name)
            if _path.isfile(file_path):
                _unlink(file_path)


class CleanupOldSessions(Abstract):
    """Cleanup Old Session Files Command.
    """
    def get_name(self) -> str:
        return 'app:cleanup:session'

    def get_description(self):
        from pytsite.core.lang import t
        return t('pytsite.core@cleanup_session_console_command_description')

    def execute(self, **kwargs: dict):
        session_dir = _reg.get('paths.session')
        ttl = int(_reg.get('session.ttl', 21600))  # 6 hours
        for file_name in _listdir(session_dir):
            file_path = _path.join(session_dir, file_name)
            if _path.isfile(file_path) and (_time() - _path.getmtime(file_path)) >= ttl:
                _unlink(file_path)


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
        if _path.exists(lock_path):
            raise Exception('Lock file exists.')

        self._lock_file_op(True)

        d = self._get_descriptor()
        now = _datetime.now()
        for evt in 'hourly', 'daily', 'weekly', 'monthly':
            delta = now - d[evt]
            if evt == 'hourly' and delta.total_seconds() >= 3600 \
                    or evt == 'daily' and delta.total_seconds() >= 86400 \
                    or evt == 'weekly' and delta.total_seconds() >= 604800 \
                    or evt == 'monthly' and delta.total_seconds() >= 2592000:
                _events.fire('pytsite.core.cron.' + evt)
                self._update_descriptor(evt)

        self._lock_file_op(False)

    @staticmethod
    def _get_descriptor_file_path():
        """Get descriptor file path.
        """
        return _path.join(_reg.get('paths.storage'), 'cron.data')

    @staticmethod
    def _get_lock_file_path() -> str:
        """Get lock file path.
        """
        return _path.join(_reg.get('paths.storage'), 'cron.lock')

    def _lock_file_op(self, op: bool):
        """Operation with lock file.
        """
        file_path = self._get_lock_file_path()
        if op:
            with open(file_path, 'wt') as f:
                f.write(_datetime.now().isoformat())
        elif _path.exists(file_path):
            _unlink(file_path)

    def _get_descriptor(self) -> dict:
        """Get descriptor info.
        """
        data = None
        file_path = self._get_descriptor_file_path()
        if not _path.exists(file_path):
            data = {
                'hourly': _datetime.fromtimestamp(0),
                'daily': _datetime.fromtimestamp(0),
                'weekly': _datetime.fromtimestamp(0),
                'monthly': _datetime.fromtimestamp(0),
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
        data[part] = _datetime.now()
        with open(self._get_descriptor_file_path(), 'wb') as f:
            pickle.dump(data, f)

        return data


class Maintenance(Abstract):
    """Maintenance Command.
    """
    def get_name(self) -> str:
        """Get name of the command.
        """
        return 'app:maintenance'

    def get_description(self) -> str:
        """Get description of the command.
        """
        from pytsite.core.lang import t
        return t('pytsite.core@maintenance_console_command_description')

    def execute(self, **kwargs: dict):
        """Execute the command.
        """
        from pytsite.core.lang import t
        from . import _functions
        lock_path = _reg.get('paths.maintenance.lock')

        if 'enable' in kwargs:
            with open(lock_path, 'wt') as f:
                f.write(str(_datetime.now()))
            _functions.print_success(t('pytsite.core@maintenance_mode_enabled'))

        if 'disable' in kwargs:
            _unlink(lock_path)
            _functions.print_success(t('pytsite.core@maintenance_mode_disabled'))


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

        lock_path = _reg.get('paths.setup.lock')
        if _path.exists(lock_path):
            raise _error.ConsoleRuntimeError(t('pytsite.core@setup_already_completed'))

        _events.fire('app.setup')

        # Writing lock file
        lock_dir = _path.dirname(lock_path)
        if not _path.isdir(lock_dir):
            _makedirs(lock_dir, 0o755, True)
        with open(lock_path, 'wt') as f:
            f.write(_datetime.now().isoformat())

        from ._functions import print_info
        print_info(t('pytsite.core@setup_has_been_completed'))

class Update(Abstract):
    """Setup Command.
    """
    def get_name(self) -> str:
        """Get name of the command.
        """
        return 'app:update'

    def get_description(self) -> str:
        """Get description of the command.
        """
        from pytsite.core.lang import t
        return t('pytsite.core@update_console_command_description')

    def execute(self, **kwargs: dict):
        """Execute the command.
        """
        from . import _functions

        _functions.run_command('app:maintenance', enable=True)
        _events.fire('app.update')
        _functions.run_command('app:maintenance', disable=True)
