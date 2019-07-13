"""PytSite Logger Events Handlers
"""
__author__ = 'Oleksandr Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

from pytsite import util, reg, logger


def cleanup():
    success, failed = util.cleanup_files(reg.get('paths.log'), reg.get('logger.file_ttl', 2592000))  # 30d

    for f_path in success:
        logger.debug('Obsolete log file removed: {}'.format(f_path))

    for f_path, e in failed:
        logger.error('Error while removing obsolete log file {}: {}'.format(f_path, e))
