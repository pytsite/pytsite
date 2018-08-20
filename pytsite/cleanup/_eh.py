"""PytSite Cleanup Event Handlers
"""
__author__ = 'Oleksandr Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

from pytsite import logger as _logger, reg as _reg, events as _events, util as _util


def cron_hourly():
    _cleanup_tmp_files()

    _events.fire('pytsite.cleanup@cleanup')


def _cleanup_tmp_files():
    success, failed = _util.cleanup_files(_reg.get('paths.tmp'), 86400)  # 24h

    for f_path in success:
        _logger.debug('Obsolete tmp file removed: {}'.format(f_path))

    for f_path, e in failed:
        _logger.error('Error while removing obsolete tmp file {}: {}'.format(f_path, e))
