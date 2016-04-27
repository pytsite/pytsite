"""PytSite Cron.
"""
from datetime import datetime as _datetime
from pytsite import events as _events, reg as _reg, logger as _logger, cache as _cache, mp as _mp

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


_cache_pool = _cache.create_pool('pytsite.cron')


def _get_lock() -> _mp.Lock:
    """Get cron global lock.
    """
    return _mp.get_lock('pytsite.cron')


def _get_stats() -> dict:
    """Get stats.
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
    """Update descriptor.
    """
    data = _get_stats()
    data[part] = _datetime.now()

    _cache_pool.put('stats', data)

    return data


if _reg.get('env.type') == 'uwsgi' and _reg.get('cron.enabled', True):
    from uwsgidecorators import timer as _uwsgi_timer

    @_uwsgi_timer(60)
    def _cron_worker(num):
        """Cron worker.
        """
        # Global lock is necessary in multi-server applications
        lock = _get_lock()

        # Start worker only if no other worker running
        if lock.locked():
            _logger.warn('Cron is still working.', __name__)
            return

        try:
            # Locking maximum for 10 minutes to prevent long lived deadlocks
            lock.lock(600)

            # Starting worker
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

                        _logger.info('Cron event: pytsite.cron.' + evt, __name__)

                        try:
                            _events.fire('pytsite.cron.' + evt)
                        except Exception as e:
                            _logger.error('{}'.format(str(e)), __name__)
                        finally:
                            _update_stats(evt)
                else:
                    _update_stats(evt)

        finally:
          lock.unlock()
