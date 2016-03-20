"""PytSite Cron.
"""
from time import sleep as _sleep
from datetime import datetime as _datetime
from pytsite import events as _events, reg as _reg, threading as _threading, logger as _logger, cache as _cache, \
    mp as _mp

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


_cache_pool = _cache.create_pool('pytsite.cron', _reg.get('cron.cache.driver', 'redis'))


def _cron_worker():
    """Start the cron.
    """
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


def _get_stats() -> dict:
    """Get stats.
    """
    stats = _cache_pool.get('stats')

    if not stats:
        zero = _datetime.fromtimestamp(0)
        stats = {
            '1min': zero,
            '5min': zero,
            '15min': zero,
            'hourly': zero,
            'daily': zero,
            'weekly': zero,
            'monthly': zero,
        }

    return stats


def _update_stats(part: str) -> dict:
    """Update descriptor.
    """
    data = _get_stats()
    data[part] = _datetime.now()

    _cache_pool.put('stats', data)

    return data


def _get_lock() -> _mp.Lock:
    return _mp.get_lock('pytsite.cron')


def _cron_thread():
    _logger.info('Cron main thread started.', __name__)

    while True:
        lock = _get_lock()

        # Check if cron is still works
        if not lock.locked():
            try:
                lock.lock(600)
                _cron_worker()
            finally:
                lock.unlock()
        else:
            _logger.warn('Cron is still working.', __name__)

        _sleep(60)


def is_started() -> bool:
    return _get_lock().locked()


# Start cron right after module initialization
if _reg.get('env.type') == 'uwsgi' and _reg.get('cron.enabled', True):
    _threading.create_thread(_cron_thread).start()
