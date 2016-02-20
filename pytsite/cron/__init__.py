"""PytSite Cron.
"""
import pickle as _pickle
from os import path as _path
from time import sleep as _sleep
from datetime import datetime as _datetime, timedelta as _timedelta
from pytsite import events as _events, reg as _reg, threading as _threading, logger as _logger

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


_stats = None
_working = False


def _cron_task():
    """Start the cron.
    """
    global _working

    _working = True
    _events.fire('pytsite.cron.tick')

    stats = _get_stats()
    now = _datetime.now()
    for evt in '1min', '5min', '15min', '30min', 'hourly', 'daily', 'weekly', 'monthly':
        if evt in stats:
            delta = now - stats[evt]
            if (evt == '1min' and delta.total_seconds() >= 60) \
                    or (evt == '5min' and delta.total_seconds() >= 300) \
                    or (evt == '15min' and delta.total_seconds() >= 900) \
                    or (evt == '30min' and delta.total_seconds() >= 1800) \
                    or (evt == 'hourly' and delta.total_seconds() >= 3600) \
                    or (evt == 'daily' and delta.total_seconds() >= 86400) \
                    or (evt == 'weekly' and delta.total_seconds() >= 604800) \
                    or (evt == 'monthly' and delta.total_seconds() >= 2592000):

                _logger.info('Cron event: pytsite.cron.' + evt, __name__)

                try:
                    _events.fire('pytsite.cron.' + evt)
                except Exception as e:
                    _logger.error('{}'.format(str(e)), __name__)
                finally:
                    _update_stats(evt)
        else:
            _update_stats(evt)

    _working = False


def _get_stats_file_path():
    """Get descriptor file path.
    """
    return _path.join(_reg.get('paths.storage'), 'cron.data')


def _get_stats() -> dict:
    """Get descriptor info.
    """
    global _stats

    if not _stats:
        file_path = _get_stats_file_path()
        if not _path.exists(file_path):
            data = {
                '1min': _datetime.fromtimestamp(0),
                '5min': _datetime.fromtimestamp(0),
                '15min': _datetime.fromtimestamp(0),
                'hourly': _datetime.fromtimestamp(0),
                'daily': _datetime.fromtimestamp(0),
                'weekly': _datetime.fromtimestamp(0),
                'monthly': _datetime.fromtimestamp(0),
            }
            with open(file_path, 'wb') as f:
                _pickle.dump(data, f)
        else:
            with open(file_path, 'rb') as f:
                data = _pickle.load(f)

        _stats = data

    return _stats


def _update_stats(part: str) -> dict:
    """Update descriptor.
    """
    data = _get_stats()
    data[part] = _datetime.now()
    with open(_get_stats_file_path(), 'wb') as f:
        _pickle.dump(data, f)

    global _stats
    _stats = data

    return _stats


def _cron_main_thread():
    _logger.info('Cron main thread started.', __name__)

    while True:
        if not _working:
            _cron_task()
        else:
            _logger.warn('Cron is still working.', __name__)

        _sleep(60)

if _reg.get('env.type') == 'uwsgi' and _reg.get('cron.enabled', True):
    _threading.create_thread(_cron_main_thread).start()
