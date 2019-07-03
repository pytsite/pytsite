"""PytSite Cleanup Event Handlers
"""
__author__ = 'Oleksandr Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

from pytsite import logger, reg, events, util


def cron_hourly():
    _cleanup_tmp_files()

    events.fire('pytsite.cleanup@cleanup')


def _cleanup_tmp_files():
    success, failed = util.cleanup_files(reg.get('paths.tmp'), 86400)  # 24h

    for f_path in success:
        logger.debug('Obsolete temporary file removed: {}'.format(f_path))

    for f_path, e in failed:
        logger.error('Error while removing obsolete tmp file {}: {}'.format(f_path, e))
