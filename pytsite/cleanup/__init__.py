"""PytSite Cleanup
"""
__author__ = 'Oleksandr Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


# Public API
def on_cleanup(handler, priority: int = 0):
    from pytsite import events
    events.listen('pytsite.cleanup@cleanup', handler, priority)


def _init():
    from pytsite import cron
    from . import _eh

    # Events handlers
    cron.hourly(_eh.cron_hourly)


_init()
