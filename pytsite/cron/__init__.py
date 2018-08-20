"""PytSite Cron
"""
__author__ = 'Oleksandr Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

# Public API
from ._api import on_start, on_stop, every_min, every_5min, every_15min, every_30min, hourly, daily, weekly, monthly

from datetime import datetime as _datetime
from time import time as _time
from pytsite import events as _events, reg as _reg, logger as _logger, cache as _cache, threading as _threading, \
    maintenance as _maintenance

_cache_pool = _cache.create_pool('pytsite.cron')
_DEBUG = _reg.get('cron.debug', False)
_LOCK_TTL = _reg.get('cron.lock_ttl', 3600)


def _get_stats() -> dict:
    """Get stats
    """
    if _cache_pool.has('stats'):
        stats = _cache_pool.get('stats')

    else:
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
    """Update stats
    """
    data = _get_stats()
    data[part] = _datetime.now()

    _cache_pool.put('stats', data)

    return data


def _cron_worker():
    """Cron worker
    """
    try:
        # Check maintenance mode
        if _maintenance.is_enabled():
            _logger.warn('Cron worker cannot start due to maintenance mode enabled')
            return

        _events.fire('pytsite.cron@start')

        # Check lock
        try:
            lock_time = _cache_pool.get('lock')

            # Double check key's creation time, because cache driver may depend from cron
            if _time() - lock_time >= _LOCK_TTL:
                _logger.warn('Obsolete cache lock removed')
                _cache_pool.rm('lock')
            else:
                _logger.warn('Cron is still working')
                return

        # Lock does not exist
        except _cache.error.KeyNotExist:
            pass

        # Create lock
        lock_time = _time()
        _cache_pool.put('lock', lock_time, _LOCK_TTL)
        if _DEBUG:
            _logger.debug('Cron lock created with TTL == {}'.format(_LOCK_TTL))

        stats = _get_stats()
        now = _datetime.now()
        for evt in '1min', '5min', '15min', '30min', 'hourly', 'daily', 'weekly', 'monthly':
            if evt in stats:
                delta = now - stats[evt]
                if (evt == '1min' and delta.total_seconds() >= 59) \
                        or (evt == '5min' and delta.total_seconds() >= 299) \
                        or (evt == '15min' and delta.total_seconds() >= 899) \
                        or (evt == '30min' and delta.total_seconds() >= 1799) \
                        or (evt == 'hourly' and delta.total_seconds() >= 3600) \
                        or (evt == 'daily' and delta.total_seconds() >= 86400) \
                        or (evt == 'weekly' and delta.total_seconds() >= 604800) \
                        or (evt == 'monthly' and delta.total_seconds() >= 2592000):

                    if _DEBUG:
                        _logger.debug('Cron event: pytsite.cron@' + evt)

                    try:
                        _events.fire('pytsite.cron@' + evt, True)

                    except Exception as e:
                        _logger.error(e)

                    finally:
                        _update_stats(evt)
            else:
                _update_stats(evt)

    finally:
        _events.fire('pytsite.cron@stop')

        # Unlock
        _cache_pool.rm('lock')
        if _DEBUG:
            _logger.debug('Cron lock removed')

        # Schedule next start
        _threading.run_in_thread(_cron_worker, 60)
        if _DEBUG:
            _logger.debug('Next cron start scheduled')


if _reg.get('env.type') == 'wsgi' and _reg.get('cron.enabled', True):
    _threading.run_in_thread(_cron_worker, 60)
