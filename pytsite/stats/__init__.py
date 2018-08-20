"""PytSite Stats
"""
from ._api import on_update

__author__ = 'Oleksandr Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


def _init():
    from pytsite import reg, cron

    if reg.get('debug'):
        from . import _eh
        cron.every_min(_eh.cron_every_min)


_init()
