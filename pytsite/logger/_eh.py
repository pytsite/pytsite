"""PytSite Logger Events Handlers
"""

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

from pytsite import util as _util, reg as _reg, logger as _logger


def cleanup():
    success, failed = _util.cleanup_files(_reg.get('paths.log'), _reg.get('logger.file_ttl', 2592000))  # 30d

    for f_path in success:
        _logger.debug('Obsolete log file removed: {}'.format(f_path))

    for f_path, e in failed:
        _logger.error('Error while removing obsolete log file {}: {}'.format(f_path, e))
