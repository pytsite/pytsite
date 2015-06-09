"""Cron.
"""
__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

import pickle
from os import path, unlink
from datetime import datetime
from pytsite.core import reg, events, console, lang


class CronCommand(console.AbstractCommand):
    """Cron command.
    """
    def get_name(self):
        """Get command name.
        """

        return 'cron:start'

    def get_description(self):
        """Get command description.
        """

        return lang.t('pytsite.core@cron_console_command_description')

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
