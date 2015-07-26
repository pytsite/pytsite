"""PytSite Cron.
"""
__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

import pickle as _pickle
import threading as _threading
from os import path as _path
from sys import modules as _modules
from datetime import datetime as _datetime, timedelta as _timedelta
from pytsite.core import events as _events, logger as _logger, reg as _reg


def _start():
    """Start the cron.
    """
    _logger.info(__name__ + '. Cron start.')

    d = _get_descriptor()
    now = _datetime.now()
    for evt in '15min', 'hourly', 'daily', 'weekly', 'monthly':
        delta = now - d[evt]
        if evt == '15min' and delta.total_seconds() >= 900 \
                or evt == 'hourly' and delta.total_seconds() >= 3600 \
                or evt == 'daily' and delta.total_seconds() >= 86400 \
                or evt == 'weekly' and delta.total_seconds() >= 604800 \
                or evt == 'monthly' and delta.total_seconds() >= 2592000:

            _logger.info(__name__ + '. Cron event: ' + evt)

            try:
                _events.fire('pytsite.core.cron.' + evt)
            except Exception as e:
                _logger.error('{}. {}'.format(__name__, str(e)))
            finally:
                _update_descriptor(evt)

    _logger.info(__name__ + '. Cron stop.')

    # Every 15 min
    _threading.Timer(900, _modules[__name__]._start).start()
    _logger.info('{}. Next cron start scheduled at {}'\
                  .format(__name__, str(_datetime.now() + _timedelta(seconds=900))))


def _get_descriptor_file_path():
    """Get descriptor file path.
    """
    return _path.join(_reg.get('paths.storage'), 'cron.data')


def _get_descriptor() -> dict:
    """Get descriptor info.
    """
    file_path = _get_descriptor_file_path()
    if not _path.exists(file_path):
        data = {
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

    return data


def _update_descriptor(part: str) -> dict:
    """Update descriptor.
    """
    data = _get_descriptor()
    data[part] = _datetime.now()
    with open(_get_descriptor_file_path(), 'wb') as f:
        _pickle.dump(data, f)

    return data

# Start
if _reg.get('cron.enabled'):
    _start()
