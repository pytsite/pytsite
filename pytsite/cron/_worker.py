"""Cron Worker
"""
__author__ = 'Oleksandr Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

from datetime import datetime
from time import time
from pytsite import events, reg, logger, cache, threading, maintenance

EVENT_NAMES = ['1min', '5min', '15min', 'hourly', 'daily', 'weekly', 'monthly']

_cache_pool = cache.create_pool('pytsite.cron')
_DEBUG = reg.get('cron.debug', False)
_LOCK_TTL = reg.get('cron.lock_ttl', 3600)


def _get_stats() -> dict:
    """Get stats
    """
    if _cache_pool.has('stats'):
        stats = _cache_pool.get('stats')
    else:
        zero = datetime.fromtimestamp(0)
        stats = {k: zero for k in EVENT_NAMES}

    return stats


def _update_stats(part: str) -> dict:
    """Update stats
    """
    data = _get_stats()
    data[part] = datetime.now()

    _cache_pool.put('stats', data)

    return data


def worker(event_name: str = None, schedule_next: bool = True, force: bool = False):
    """Cron worker
    """
    if event_name:
        if event_name not in EVENT_NAMES:
            raise ValueError(f"Cron event '{event_name}' is not supported")
        event_names = [event_name]
    else:
        event_names = EVENT_NAMES

    try:
        # Check maintenance mode
        if maintenance.is_enabled():
            logger.warn('Cron worker cannot start due to maintenance mode enabled')
            return

        events.fire('pytsite.cron@start')

        # Check lock
        try:
            lock_time = _cache_pool.get('lock')

            # Double check key's creation time, because cache driver may depend from cron
            if time() - lock_time >= _LOCK_TTL:
                logger.warn('Obsolete cron lock removed')
                _cache_pool.rm('lock')
            else:
                logger.warn('Cron is still working')
                return

        # Lock does not exist
        except cache.error.KeyNotExist:
            pass

        # Create lock
        lock_time = time()
        _cache_pool.put('lock', lock_time, _LOCK_TTL)
        if _DEBUG:
            logger.debug('Cron lock created with TTL == {}'.format(_LOCK_TTL))

        stats = _get_stats()
        now = datetime.now()
        for evt in event_names:
            if evt in stats:
                ds = (now - stats[evt]).total_seconds()
                if force \
                        or (evt == '1min' and ds >= 59) \
                        or (evt == '5min' and ds >= 299) \
                        or (evt == '15min' and ds >= 899) \
                        or (evt == '30min' and ds >= 1799) \
                        or (evt == 'hourly' and ds >= 3600) \
                        or (evt == 'daily' and ds >= 86400) \
                        or (evt == 'weekly' and ds >= 604800) \
                        or (evt == 'monthly' and ds >= 2592000):

                    if _DEBUG:
                        logger.debug('Cron event: pytsite.cron@' + evt)

                    try:
                        events.fire('pytsite.cron@' + evt, True)
                    except Exception as e:
                        logger.error(e)
                    finally:
                        _update_stats(evt)
            else:
                _update_stats(evt)

    finally:
        events.fire('pytsite.cron@stop')

        # Unlock
        _cache_pool.rm('lock')
        if _DEBUG:
            logger.debug('Cron lock removed')

        # Schedule next start
        if schedule_next:
            threading.run_in_thread(worker, 60)
            if _DEBUG:
                logger.debug('Next cron start scheduled')
