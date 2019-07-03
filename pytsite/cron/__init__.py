"""PytSite Cron
"""
__author__ = 'Oleksandr Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

# Public API
from ._api import on_start, on_stop, every_min, every_5min, every_15min, every_30min, hourly, daily, weekly, monthly


def _init():
    from pytsite import reg, lang, threading, console
    from . import _worker, _console

    lang.register_package(__name__)
    console.register_command(_console.Run())

    if reg.get('env.type') == 'wsgi' and reg.get('cron.enabled', True):
        threading.run_in_thread(_worker.worker, 60)


_init()
