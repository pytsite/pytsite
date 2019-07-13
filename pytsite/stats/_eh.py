"""PytSite Stats Event Handlers
"""
__author__ = 'Oleksandr Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

from os import path
from pytsite import events, reg, logger, util


def cron_every_min():
    out = ''
    for r in events.fire('pytsite.stats@update'):
        if not r or not isinstance(r, str):
            continue

        out += '- ' + r + '\n'

    with open(path.join(reg.get('paths.storage'), 'stats.txt'), 'wt') as f:
        f.write(util.w3c_datetime_str() + '\n\n' + out)

    if out:
        logger.info('Current stats:\n{}'.format(out[:-1]))
