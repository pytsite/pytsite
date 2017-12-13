"""PytSite Stats Event Handlers
"""
from os import path as _path
from pytsite import events as _events, reg as _reg, logger as _logger, util as _util

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


def cron_every_min():
    out = ''
    for r in _events.fire('pytsite.stats@update'):
        if not r or not isinstance(r, str):
            continue

        out += '- ' + r + '\n'

    with open(_path.join(_reg.get('paths.storage'), 'stats.txt'), 'wt') as f:
        f.write(_util.w3c_datetime_str() + '\n\n' + out)

    if out:
        _logger.info('Current stats:\n{}'.format(out[:-1]))
