"""PytSite Cron.
"""
from datetime import datetime as _datetime
from pytsite import events as _events, reg as _reg, logger as _logger, cache as _cache, auth as _auth, \
    threading as _threading
from ._api import every_min, every_5min, every_15min, every_30min, hourly, daily, weekly, monthly

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

_cache_pool = _cache.create_pool('pytsite.cron')
_working = False


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


def _cron_worker():
    """Cron worker.
    """
    global _working

    # Check lock
    if _working:
        _logger.warn('Cron is still working')
        return

    try:
        # Lock
        _working = True

        # Disable permission checking
        _auth.switch_user_to_system()

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

                    _logger.info('Cron event: pytsite.cron.' + evt)

                    try:
                        _events.fire('pytsite.cron.' + evt)
                    except RuntimeWarning as e:
                        _logger.warn(str(e), exc_info=e, stack_info=True)
                    except Exception as e:
                        _logger.error(str(e), exc_info=e, stack_info=True)
                    finally:
                        _update_stats(evt)
            else:
                _update_stats(evt)

        # Enable permissions checking
        _auth.restore_user()

    finally:
        # Unlock
        _working = False


if _reg.get('env.type') == 'uwsgi' and _reg.get('cron.enabled', True):
    import uwsgidecorators


    @uwsgidecorators.timer(60)
    def cron_thread(n):
        _threading.create_thread(_cron_worker).start()
